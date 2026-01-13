# Station 3.2 - Voice WebSocket with Barge-In

## Overview
Implement real-time voice WebSocket with Voice Activity Detection (VAD) and barge-in support. Allow users to interrupt AI responses mid-speech, creating natural conversation flow.

## Learning Objectives
- Build WebSocket-based real-time audio streaming
- Implement Voice Activity Detection (VAD)
- Handle barge-in (user interrupting AI)
- Manage concurrent voice sessions
- Coordinate asyncio tasks for audio processing

---

## 🎯 GENERATION PROMPT

Create real-time voice WebSocket with barge-in for Atomic Cat AI:

**File: voice-server/voice_websocket.py**

```python
import asyncio
import json
import logging
import numpy as np
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
from fastapi import WebSocket, WebSocketDisconnect
from enum import Enum
import struct

logger = logging.getLogger(__name__)

class SessionState(Enum):
    """Voice session states"""
    IDLE = "idle"
    LISTENING = "listening"
    PROCESSING = "processing"
    SPEAKING = "speaking"

@dataclass
class VoiceSession:
    """Represents an active voice session"""
    session_id: str
    websocket: WebSocket
    user_id: str
    state: SessionState = SessionState.IDLE
    audio_buffer: list = field(default_factory=list)
    tts_task: Optional[asyncio.Task] = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def __post_init__(self):
        self.vad = SimpleVAD()
    
    async def cancel_tts(self):
        """Cancel ongoing TTS playback"""
        if self.tts_task and not self.tts_task.done():
            self.tts_task.cancel()
            try:
                await self.tts_task
            except asyncio.CancelledError:
                logger.info(f"TTS cancelled for session {self.session_id}")
                pass

class VoiceSessionManager:
    """Manage concurrent voice sessions"""
    
    def __init__(self, max_sessions: int = 4):
        self.sessions: Dict[str, VoiceSession] = {}
        self.max_sessions = max_sessions
    
    def add_session(self, session: VoiceSession) -> bool:
        """Add new session if capacity available"""
        if len(self.sessions) >= self.max_sessions:
            return False
        self.sessions[session.session_id] = session
        logger.info(f"Session added: {session.session_id} (total: {len(self.sessions)})")
        return True
    
    def remove_session(self, session_id: str):
        """Remove session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            logger.info(f"Session removed: {session_id} (total: {len(self.sessions)})")
    
    def get_session(self, session_id: str) -> Optional[VoiceSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def get_stats(self) -> dict:
        """Get session statistics"""
        return {
            "active_sessions": len(self.sessions),
            "max_sessions": self.max_sessions,
            "sessions": [
                {
                    "id": s.session_id,
                    "user_id": s.user_id,
                    "state": s.state.value,
                    "duration": (datetime.now() - s.created_at).total_seconds()
                }
                for s in self.sessions.values()
            ]
        }

class SimpleVAD:
    """Simple energy-based Voice Activity Detection"""
    
    def __init__(self, threshold: float = 0.02, sample_rate: int = 16000):
        self.threshold = threshold
        self.sample_rate = sample_rate
        self.silence_duration = 0.0
        self.min_speech_duration = 0.3  # 300ms minimum speech
        self.max_silence_duration = 1.5  # 1.5s silence = end of speech
        self.frame_duration = 0.03  # 30ms frames
        self.is_speaking = False
        self.speech_start_time = None
    
    def compute_energy(self, audio_frame: np.ndarray) -> float:
        """Compute RMS energy of audio frame"""
        return np.sqrt(np.mean(audio_frame ** 2))
    
    def detect(self, audio_frame: np.ndarray) -> dict:
        """
        Detect voice activity in audio frame
        
        Returns:
            dict with 'is_speech', 'speech_start', 'speech_end'
        """
        energy = self.compute_energy(audio_frame)
        
        result = {
            "is_speech": False,
            "speech_start": False,
            "speech_end": False,
            "energy": float(energy)
        }
        
        if energy > self.threshold:
            # Speech detected
            if not self.is_speaking:
                # Speech just started
                self.is_speaking = True
                self.speech_start_time = datetime.now()
                result["speech_start"] = True
                logger.debug("Speech started")
            
            self.silence_duration = 0.0
            result["is_speech"] = True
        else:
            # Silence detected
            if self.is_speaking:
                self.silence_duration += self.frame_duration
                
                # Check if silence is long enough to end speech
                if self.silence_duration >= self.max_silence_duration:
                    speech_duration = (datetime.now() - self.speech_start_time).total_seconds()
                    
                    # Only end if minimum speech duration met
                    if speech_duration >= self.min_speech_duration:
                        self.is_speaking = False
                        result["speech_end"] = True
                        logger.debug(f"Speech ended (duration: {speech_duration:.2f}s)")
        
        return result

# Global session manager
session_manager = VoiceSessionManager(max_sessions=4)

async def voice_websocket_handler(
    websocket: WebSocket,
    session_id: str,
    user_id: str,
    voice_model
):
    """
    Handle voice WebSocket connection with barge-in support
    
    Flow:
    1. User sends audio chunks (PCM, 16kHz, 16-bit)
    2. VAD detects speech start/end
    3. On speech end, transcribe and process
    4. Send response audio back
    5. If user speaks during AI response, trigger barge-in
    """
    
    # Create session
    session = VoiceSession(
        session_id=session_id,
        websocket=websocket,
        user_id=user_id
    )
    
    # Check capacity
    if not session_manager.add_session(session):
        await websocket.send_json({
            "type": "error",
            "message": "Server at maximum capacity. Please try again later."
        })
        await websocket.close()
        return
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "session_id": session_id,
            "message": "Voice session established"
        })
        
        # Main message loop
        while True:
            # Receive audio data or commands
            data = await websocket.receive()
            
            if "bytes" in data:
                # Audio chunk received
                audio_bytes = data["bytes"]
                await handle_audio_chunk(session, audio_bytes, voice_model)
            
            elif "text" in data:
                # JSON command received
                message = json.loads(data["text"])
                await handle_command(session, message, voice_model)
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected: {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e)
            })
        except:
            pass
    finally:
        # Cleanup
        await session.cancel_tts()
        session_manager.remove_session(session_id)

async def handle_audio_chunk(
    session: VoiceSession,
    audio_bytes: bytes,
    voice_model
):
    """Process incoming audio chunk with VAD"""
    
    # Convert bytes to numpy array (16-bit PCM)
    audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    
    # Check for barge-in: user speaking while AI is speaking
    if session.state == SessionState.SPEAKING:
        vad_result = session.vad.detect(audio_array)
        
        if vad_result["is_speech"]:
            # Barge-in detected!
            logger.info(f"Barge-in detected in session {session.session_id}")
            
            # Cancel ongoing TTS
            await session.cancel_tts()
            
            # Notify client
            await session.websocket.send_json({
                "type": "barge_in",
                "message": "User interrupted, cancelling response"
            })
            
            # Switch to listening
            session.state = SessionState.LISTENING
            session.audio_buffer = []
    
    # Handle normal listening
    if session.state in [SessionState.IDLE, SessionState.LISTENING]:
        vad_result = session.vad.detect(audio_array)
        
        if vad_result["speech_start"]:
            # User started speaking
            session.state = SessionState.LISTENING
            session.audio_buffer = []
            
            await session.websocket.send_json({
                "type": "listening",
                "message": "Listening..."
            })
        
        if vad_result["is_speech"]:
            # Accumulate speech audio
            session.audio_buffer.append(audio_array)
        
        if vad_result["speech_end"]:
            # User finished speaking, process
            logger.info(f"Speech ended in session {session.session_id}, transcribing...")
            
            session.state = SessionState.PROCESSING
            
            await session.websocket.send_json({
                "type": "processing",
                "message": "Processing..."
            })
            
            # Concatenate audio buffer
            if session.audio_buffer:
                full_audio = np.concatenate(session.audio_buffer)
                session.audio_buffer = []
                
                # Transcribe
                try:
                    text = voice_model.transcribe(full_audio)
                    logger.info(f"Transcribed: {text}")
                    
                    await session.websocket.send_json({
                        "type": "transcription",
                        "text": text
                    })
                    
                    # TODO: Get LLM response (integrate with middleware)
                    # For now, echo back
                    response_text = f"You said: {text}"
                    
                    # Synthesize response
                    await synthesize_and_play(session, response_text, voice_model)
                
                except Exception as e:
                    logger.error(f"Processing error: {e}")
                    await session.websocket.send_json({
                        "type": "error",
                        "message": "Failed to process audio"
                    })
                    session.state = SessionState.IDLE

async def synthesize_and_play(
    session: VoiceSession,
    text: str,
    voice_model
):
    """Synthesize text to speech and stream to client"""
    
    session.state = SessionState.SPEAKING
    
    await session.websocket.send_json({
        "type": "speaking",
        "message": "Speaking..."
    })
    
    async def tts_task():
        """TTS playback task (can be cancelled)"""
        try:
            # Synthesize audio
            audio_bytes = voice_model.synthesize(text)
            
            # Stream audio in chunks (simulate streaming TTS)
            chunk_size = 4096
            for i in range(0, len(audio_bytes), chunk_size):
                chunk = audio_bytes[i:i+chunk_size]
                
                # Send audio chunk
                await session.websocket.send_bytes(chunk)
                
                # Small delay to simulate real-time playback
                await asyncio.sleep(0.05)
            
            # TTS completed
            await session.websocket.send_json({
                "type": "speaking_end",
                "message": "Response complete"
            })
            
            session.state = SessionState.IDLE
        
        except asyncio.CancelledError:
            # Task was cancelled (barge-in)
            raise
        except Exception as e:
            logger.error(f"TTS error: {e}")
            await session.websocket.send_json({
                "type": "error",
                "message": "TTS failed"
            })
            session.state = SessionState.IDLE
    
    # Start TTS task (stored in session for cancellation)
    session.tts_task = asyncio.create_task(tts_task())
    
    try:
        await session.tts_task
    except asyncio.CancelledError:
        # Task was cancelled, handle cleanup
        await session.websocket.send_json({
            "type": "tts_cancelled",
            "message": "Response cancelled"
        })
        session.state = SessionState.IDLE

async def handle_command(
    session: VoiceSession,
    message: dict,
    voice_model
):
    """Handle JSON commands from client"""
    
    cmd_type = message.get("type")
    
    if cmd_type == "ping":
        await session.websocket.send_json({
            "type": "pong"
        })
    
    elif cmd_type == "reset":
        # Reset VAD state
        session.vad = SimpleVAD()
        session.audio_buffer = []
        session.state = SessionState.IDLE
        
        await session.websocket.send_json({
            "type": "reset_complete"
        })
    
    elif cmd_type == "cancel":
        # Cancel any ongoing operations
        await session.cancel_tts()
        session.state = SessionState.IDLE
        
        await session.websocket.send_json({
            "type": "cancelled"
        })
```

**Add to voice-server/server.py**:
```python
from voice_websocket import voice_websocket_handler, session_manager

@app.websocket("/ws/voice/{session_id}")
async def voice_websocket(websocket: WebSocket, session_id: str, user_id: str):
    """Voice WebSocket endpoint"""
    await voice_websocket_handler(websocket, session_id, user_id, voice_model)

@app.get("/sessions")
async def get_sessions():
    """Get active voice session statistics"""
    return session_manager.get_stats()
```

**Requirements**:
1. VoiceSession dataclass tracks all session state
2. VoiceSessionManager limits concurrent sessions (max 4)
3. SimpleVAD uses energy-based detection with configurable threshold
4. Barge-in detection: if user speaks while AI speaking, cancel TTS immediately
5. TTS runs as asyncio.Task that can be cancelled
6. Send appropriate events: listening, processing, speaking, barge_in, etc.
7. Handle CancelledError properly
8. Clean up sessions on disconnect
9. Support reset and cancel commands

**Output**: Complete voice WebSocket with barge-in support.

---

## ✅ VALIDATION PROMPT

Validate voice WebSocket with barge-in:

### Data Structures
- [ ] **VoiceSession** dataclass has:
  - session_id, websocket, user_id
  - state (SessionState enum)
  - audio_buffer (list)
  - tts_task (Optional[asyncio.Task])
  - vad (SimpleVAD instance)
- [ ] **SessionState** enum has: IDLE, LISTENING, PROCESSING, SPEAKING
- [ ] **VoiceSessionManager** manages concurrent sessions
  - max_sessions = 4
  - add_session(), remove_session(), get_session()
  - get_stats() returns session info

### SimpleVAD Class
- [ ] Energy-based voice detection
- [ ] Configurable threshold (default 0.02)
- [ ] Tracks is_speaking state
- [ ] Requires min_speech_duration (300ms)
- [ ] Requires max_silence_duration (1.5s) to end speech
- [ ] `compute_energy()` calculates RMS
- [ ] `detect()` returns dict with is_speech, speech_start, speech_end

### Barge-In Flow
Trace the complete barge-in sequence:

**Setup**: AI is speaking (state=SPEAKING, tts_task running)

**Step 1: User Starts Speaking**
- [ ] Audio chunk received
- [ ] `handle_audio_chunk()` called
- [ ] Session state is SPEAKING
- [ ] VAD detects speech (energy > threshold)

**Step 2: Barge-In Detected**
- [ ] `vad_result["is_speech"]` is True
- [ ] Logs "Barge-in detected"
- [ ] Calls `session.cancel_tts()`

**Step 3: TTS Cancellation**
- [ ] `tts_task.cancel()` called
- [ ] Task raises `asyncio.CancelledError`
- [ ] CancelledError is caught and handled
- [ ] Logs "TTS cancelled"

**Step 4: State Transition**
- [ ] Sends `barge_in` event to client
- [ ] Changes state to LISTENING
- [ ] Clears audio_buffer
- [ ] Ready for new user input

### Audio Processing
- [ ] Audio received as bytes (16-bit PCM)
- [ ] Converted to float32 numpy array (normalized to -1.0 to 1.0)
- [ ] VAD processes each chunk
- [ ] Audio accumulated in buffer during speech
- [ ] Buffer concatenated at speech end
- [ ] Transcription called with full audio

### TTS Streaming
- [ ] `synthesize_and_play()` creates TTS task
- [ ] Task stored in `session.tts_task`
- [ ] Audio synthesized first
- [ ] Then streamed in chunks (4096 bytes)
- [ ] Small delays between chunks (50ms)
- [ ] Sends `speaking_end` when complete
- [ ] Returns to IDLE state

### Task Cancellation
- [ ] `cancel_tts()` checks if task exists and not done
- [ ] Calls `task.cancel()`
- [ ] Awaits task to handle CancelledError
- [ ] Catches CancelledError without propagating

### WebSocket Events
Client receives these event types:
- [ ] `connected` - session established
- [ ] `listening` - user speech detected
- [ ] `processing` - transcribing audio
- [ ] `transcription` - text result
- [ ] `speaking` - AI starting response
- [ ] `speaking_end` - AI finished
- [ ] `barge_in` - user interrupted AI
- [ ] `tts_cancelled` - TTS stopped
- [ ] `error` - processing error
- [ ] `pong` - heartbeat response

### Commands to Test
```bash
# This requires a WebSocket client that can send audio
# Python test client:

import asyncio
import websockets
import json
import numpy as np

async def test_barge_in():
    uri = "ws://localhost:8765/ws/voice/test-session?user_id=test-user"
    
    async with websockets.connect(uri) as websocket:
        # Receive connection message
        msg = await websocket.recv()
        print(f"Connected: {msg}")
        
        # Simulate user speaking (send audio)
        # Generate 1 second of random audio (simulating speech)
        sample_rate = 16000
        duration = 1.0
        audio = np.random.randn(int(sample_rate * duration)) * 0.05
        audio_bytes = (audio * 32768).astype(np.int16).tobytes()
        
        await websocket.send(audio_bytes)
        
        # Wait for transcription
        msg = await websocket.recv()
        print(f"Transcription: {msg}")
        
        # AI will start speaking
        # Now send more audio to trigger barge-in
        await asyncio.sleep(0.5)
        
        # Send audio during AI speech (barge-in)
        await websocket.send(audio_bytes)
        
        # Should receive barge_in event
        msg = await websocket.recv()
        print(f"Barge-in: {msg}")

asyncio.run(test_barge_in())
```

### Expected Behavior
- User can interrupt AI at any time
- TTS stops immediately when interrupted
- Session transitions to listening state
- VAD detects speech start and end accurately
- Audio buffer manages memory efficiently
- Sessions limited to 4 concurrent
- Websocket errors don't crash server
- All state transitions logged

---

## Notes
- Barge-in is critical for natural conversation
- VAD threshold may need tuning per environment
- Energy-based VAD is simple but effective
- Consider more advanced VAD (WebRTC VAD, Silero VAD) for production
- TTS streaming improves perceived latency
- Next station (3.3) will integrate with middleware for LLM responses
- Session limit prevents resource exhaustion
- asyncio.Task cancellation is Python 3.7+ feature
