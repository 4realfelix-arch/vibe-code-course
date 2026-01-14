# Station 3.3 - Voice Pipeline Integration

## Overview
Integrate the voice server with the middleware to create end-to-end voice conversation: voice input → transcription → LLM response → voice output. Connect voice WebSocket to chat endpoint and memory services.

## Learning Objectives
- Connect voice processing to LLM backend
- Implement voice conversation memory
- Handle async communication between services
- Build complete voice-to-voice pipeline
- Optimize latency for real-time conversation

---

## 🎯 GENERATION PROMPT

Create complete voice pipeline integration for Atomic Cat AI:

**File: voice-server/llm_client.py**

```python
import httpx
import logging
from typing import Optional, AsyncGenerator
import json

logger = logging.getLogger(__name__)

class LLMClient:
    """Client for communicating with middleware LLM endpoint"""
    
    def __init__(self, middleware_url: str, timeout: float = 30.0):
        self.middleware_url = middleware_url.rstrip('/')
        self.timeout = timeout
    
    async def get_response(
        self,
        user_message: str,
        user_id: str,
        conversation_id: Optional[str] = None,
        stream: bool = False
    ) -> str:
        """
        Get LLM response from middleware
        
        Args:
            user_message: User's transcribed message
            user_id: User ID for authentication
            conversation_id: Optional conversation ID for context
            stream: Whether to stream response
        
        Returns:
            LLM response text
        """
        endpoint = f"{self.middleware_url}/api/chat/message"
        
        payload = {
            "message": user_message,
            "conversation_id": conversation_id,
            "stream": stream
        }
        
        headers = {
            "Authorization": f"Bearer {user_id}",  # Simplified auth
            "Content-Type": "application/json"
        }
        
        try:
            if stream:
                # Streaming response
                full_response = ""
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    async with client.stream("POST", endpoint, json=payload, headers=headers) as response:
                        response.raise_for_status()
                        
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                chunk = line[6:]
                                if chunk == "[DONE]":
                                    break
                                try:
                                    data = json.loads(chunk)
                                    content = data.get("content", "")
                                    full_response += content
                                except json.JSONDecodeError:
                                    continue
                
                return full_response
            else:
                # Non-streaming response
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(endpoint, json=payload, headers=headers)
                    response.raise_for_status()
                    data = response.json()
                    return data.get("response", "")
        
        except httpx.HTTPError as e:
            logger.error(f"LLM request failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in LLM request: {e}")
            raise

class VoiceConversationManager:
    """Manage voice conversation context and memory"""
    
    def __init__(self, llm_client: LLMClient):
        self.llm_client = llm_client
        self.conversations = {}  # session_id -> conversation_id
    
    def get_conversation_id(self, session_id: str) -> Optional[str]:
        """Get conversation ID for session"""
        return self.conversations.get(session_id)
    
    def set_conversation_id(self, session_id: str, conversation_id: str):
        """Set conversation ID for session"""
        self.conversations[session_id] = conversation_id
    
    def clear_conversation(self, session_id: str):
        """Clear conversation for session"""
        if session_id in self.conversations:
            del self.conversations[session_id]
    
    async def process_voice_message(
        self,
        user_message: str,
        user_id: str,
        session_id: str
    ) -> str:
        """
        Process voice message and get response
        
        Args:
            user_message: Transcribed user message
            user_id: User ID
            session_id: Voice session ID
        
        Returns:
            LLM response text
        """
        # Get or create conversation ID
        conversation_id = self.get_conversation_id(session_id)
        
        try:
            # Get LLM response
            response = await self.llm_client.get_response(
                user_message=user_message,
                user_id=user_id,
                conversation_id=conversation_id,
                stream=False  # Don't stream for voice (need full response for TTS)
            )
            
            # Store conversation ID if new
            if not conversation_id:
                # Conversation ID would be returned by middleware
                # For now, use session_id
                self.set_conversation_id(session_id, session_id)
            
            return response
        
        except Exception as e:
            logger.error(f"Failed to process voice message: {e}")
            # Return error message to be spoken
            return "I'm sorry, I'm having trouble processing your request right now."
```

**Update voice-server/voice_websocket.py**:

Add imports and initialization at top:
```python
from llm_client import LLMClient, VoiceConversationManager
import os

# Initialize LLM client
MIDDLEWARE_URL = os.getenv("MIDDLEWARE_URL", "http://localhost:8000")
llm_client = LLMClient(MIDDLEWARE_URL)
conversation_manager = VoiceConversationManager(llm_client)
```

Update `handle_audio_chunk()` function to integrate with LLM:
```python
# Replace the TODO section in handle_audio_chunk after transcription:

        if vad_result["speech_end"]:
            # ... existing code ...
            
            # Transcribe
            try:
                text = voice_model.transcribe(full_audio)
                logger.info(f"Transcribed: {text}")
                
                await session.websocket.send_json({
                    "type": "transcription",
                    "text": text
                })
                
                # Get LLM response using conversation manager
                response_text = await conversation_manager.process_voice_message(
                    user_message=text,
                    user_id=session.user_id,
                    session_id=session.session_id
                )
                
                logger.info(f"LLM response: {response_text}")
                
                await session.websocket.send_json({
                    "type": "response",
                    "text": response_text
                })
                
                # Synthesize and play response
                await synthesize_and_play(session, response_text, voice_model)
```

**File: voice-server/audio_utils.py**

```python
import numpy as np
import logging

logger = logging.getLogger(__name__)

class AudioBuffer:
    """Circular buffer for audio streaming"""
    
    def __init__(self, max_duration: float = 10.0, sample_rate: int = 16000):
        self.max_samples = int(max_duration * sample_rate)
        self.sample_rate = sample_rate
        self.buffer = []
        self.total_samples = 0
    
    def add(self, audio: np.ndarray):
        """Add audio to buffer"""
        self.buffer.append(audio)
        self.total_samples += len(audio)
        
        # Trim old data if exceeds max
        while self.total_samples > self.max_samples:
            removed = self.buffer.pop(0)
            self.total_samples -= len(removed)
    
    def get_all(self) -> np.ndarray:
        """Get all audio as single array"""
        if not self.buffer:
            return np.array([], dtype=np.float32)
        return np.concatenate(self.buffer)
    
    def clear(self):
        """Clear buffer"""
        self.buffer = []
        self.total_samples = 0
    
    def duration(self) -> float:
        """Get current duration in seconds"""
        return self.total_samples / self.sample_rate

class AudioChunker:
    """Split audio into fixed-size chunks for streaming"""
    
    def __init__(self, chunk_duration: float = 0.5, sample_rate: int = 16000):
        self.chunk_samples = int(chunk_duration * sample_rate)
        self.sample_rate = sample_rate
        self.remainder = np.array([], dtype=np.float32)
    
    def chunk(self, audio: np.ndarray):
        """
        Yield fixed-size chunks from audio stream
        
        Args:
            audio: Audio array to chunk
        
        Yields:
            Fixed-size audio chunks
        """
        # Combine with remainder from previous call
        if len(self.remainder) > 0:
            audio = np.concatenate([self.remainder, audio])
        
        # Yield complete chunks
        offset = 0
        while offset + self.chunk_samples <= len(audio):
            yield audio[offset:offset + self.chunk_samples]
            offset += self.chunk_samples
        
        # Store remainder
        self.remainder = audio[offset:]
    
    def flush(self):
        """Flush remaining audio"""
        if len(self.remainder) > 0:
            result = self.remainder
            self.remainder = np.array([], dtype=np.float32)
            return result
        return None

def normalize_audio(audio: np.ndarray, target_level: float = -20.0) -> np.ndarray:
    """
    Normalize audio to target dB level
    
    Args:
        audio: Audio array
        target_level: Target level in dB
    
    Returns:
        Normalized audio
    """
    # Calculate current RMS
    rms = np.sqrt(np.mean(audio ** 2))
    
    if rms < 1e-10:
        return audio
    
    # Calculate target RMS
    target_rms = 10 ** (target_level / 20.0)
    
    # Normalize
    scale = target_rms / rms
    normalized = audio * scale
    
    # Clip to prevent overflow
    normalized = np.clip(normalized, -1.0, 1.0)
    
    return normalized

def apply_noise_gate(audio: np.ndarray, threshold: float = -40.0) -> np.ndarray:
    """
    Apply noise gate to suppress background noise
    
    Args:
        audio: Audio array
        threshold: Noise gate threshold in dB
    
    Returns:
        Audio with noise gate applied
    """
    # Calculate RMS in dB
    rms = np.sqrt(np.mean(audio ** 2))
    rms_db = 20 * np.log10(rms + 1e-10)
    
    if rms_db < threshold:
        # Below threshold, suppress
        return audio * 0.0
    else:
        # Above threshold, pass through
        return audio
```

**Update voice-server/requirements.txt**:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
torch==2.1.2
torchaudio==2.1.2
numpy==1.26.3
websockets==12.0
httpx==0.26.0
```

**Add to voice-server/config.py**:
```python
import os

# Middleware integration
MIDDLEWARE_URL = os.getenv("MIDDLEWARE_URL", "http://localhost:8000")

# Audio processing
SAMPLE_RATE = int(os.getenv("SAMPLE_RATE", "16000"))
AUDIO_CHUNK_DURATION = float(os.getenv("AUDIO_CHUNK_DURATION", "0.5"))
AUDIO_NORMALIZE = os.getenv("AUDIO_NORMALIZE", "true").lower() == "true"
NOISE_GATE_THRESHOLD = float(os.getenv("NOISE_GATE_THRESHOLD", "-40"))

# Performance
MAX_AUDIO_BUFFER_DURATION = float(os.getenv("MAX_AUDIO_BUFFER_DURATION", "10.0"))
```

**Requirements**:
1. LLMClient communicates with middleware chat endpoint
2. VoiceConversationManager tracks conversation context per session
3. AudioBuffer manages audio data efficiently
4. AudioChunker splits audio into fixed-size chunks
5. Audio normalization prevents clipping
6. Noise gate suppresses background noise
7. Full pipeline: Audio → VAD → Transcription → LLM → TTS → Audio
8. Handle errors gracefully at each step
9. Optimize for low latency

**Output**: Complete voice-to-voice conversation pipeline with middleware integration.

---

## ✅ VALIDATION PROMPT

Validate voice pipeline integration:

### File Structure
- [ ] `voice-server/llm_client.py` exists
- [ ] `voice-server/audio_utils.py` exists
- [ ] `voice-server/config.py` exists
- [ ] Updates to `voice_websocket.py` for LLM integration
- [ ] `httpx` added to requirements.txt

### LLMClient Class
- [ ] `__init__()` takes middleware_url and timeout
- [ ] `get_response()` method:
  - Accepts user_message, user_id, conversation_id, stream
  - Makes POST to /api/chat/message
  - Includes Authorization header
  - Handles streaming and non-streaming
  - Returns response text
  - Handles HTTP errors gracefully

### VoiceConversationManager Class
- [ ] Tracks conversations dict (session_id → conversation_id)
- [ ] `get_conversation_id()` retrieves conversation for session
- [ ] `set_conversation_id()` stores conversation ID
- [ ] `clear_conversation()` removes conversation
- [ ] `process_voice_message()`:
  - Gets/creates conversation ID
  - Calls LLM client
  - Returns response text
  - Handles errors with fallback message

### Audio Utilities

**AudioBuffer**:
- [ ] Maintains circular buffer of audio
- [ ] Limits max duration (default 10s)
- [ ] `add()` appends audio
- [ ] `get_all()` returns concatenated array
- [ ] `clear()` resets buffer
- [ ] `duration()` returns seconds

**AudioChunker**:
- [ ] Splits audio into fixed-size chunks
- [ ] Maintains remainder between calls
- [ ] `chunk()` yields complete chunks
- [ ] `flush()` returns final remainder

**Audio Processing Functions**:
- [ ] `normalize_audio()` normalizes to target dB
- [ ] `apply_noise_gate()` suppresses below threshold
- [ ] Both handle edge cases (silence, overflow)

### Integration Flow

Trace complete voice-to-voice flow:

**Step 1: Audio Input**
- [ ] User speaks into microphone
- [ ] Audio chunks sent to WebSocket
- [ ] VAD detects speech start

**Step 2: Transcription**
- [ ] Audio accumulated in buffer
- [ ] VAD detects speech end
- [ ] Full audio transcribed to text
- [ ] Text sent to client

**Step 3: LLM Processing**
- [ ] `conversation_manager.process_voice_message()` called
- [ ] LLMClient makes request to middleware
- [ ] Middleware retrieves memories
- [ ] LLM generates response
- [ ] Response returned to voice server

**Step 4: Speech Synthesis**
- [ ] Response text synthesized to audio
- [ ] Audio streamed to client in chunks
- [ ] Client plays audio

**Step 5: Barge-In Support**
- [ ] If user speaks during playback
- [ ] VAD detects, TTS cancelled
- [ ] Flow restarts at Step 1

### Configuration
- [ ] `MIDDLEWARE_URL` environment variable
- [ ] `SAMPLE_RATE` configurable
- [ ] `AUDIO_CHUNK_DURATION` configurable
- [ ] `AUDIO_NORMALIZE` flag
- [ ] `NOISE_GATE_THRESHOLD` configurable
- [ ] `MAX_AUDIO_BUFFER_DURATION` configurable

### Error Handling
- [ ] LLM request failures return error message
- [ ] Transcription failures caught and reported
- [ ] TTS failures don't crash session
- [ ] Network errors handled gracefully
- [ ] All errors logged with context

### Commands to Test
```bash
# Set middleware URL
export MIDDLEWARE_URL=http://localhost:8000

# Start voice server
docker compose up -d voice-server middleware

# Test LLM integration (Python)
python3 << 'EOF'
import asyncio
from llm_client import LLMClient

async def test():
    client = LLMClient("http://localhost:8000")
    response = await client.get_response(
        user_message="Hello, how are you?",
        user_id="test-user",
        stream=False
    )
    print(f"Response: {response}")

asyncio.run(test())
EOF

# Test audio utilities
python3 << 'EOF'
import numpy as np
from audio_utils import AudioBuffer, AudioChunker, normalize_audio

# Test buffer
buffer = AudioBuffer(max_duration=2.0)
audio = np.random.randn(16000) * 0.1  # 1 second
buffer.add(audio)
print(f"Buffer duration: {buffer.duration():.2f}s")

# Test chunker
chunker = AudioChunker(chunk_duration=0.5)
for i, chunk in enumerate(chunker.chunk(audio)):
    print(f"Chunk {i}: {len(chunk)} samples")

# Test normalization
normalized = normalize_audio(audio, target_level=-20.0)
print(f"Original RMS: {np.sqrt(np.mean(audio**2)):.4f}")
print(f"Normalized RMS: {np.sqrt(np.mean(normalized**2)):.4f}")
EOF
```

### Performance Metrics
- [ ] End-to-end latency < 2 seconds
- [ ] Transcription: < 500ms
- [ ] LLM response: < 1000ms
- [ ] TTS: < 500ms
- [ ] Barge-in response: < 100ms

### Expected Results
- Complete voice conversation works end-to-end
- Memory context preserved across turns
- Barge-in interrupts smoothly
- Audio quality is good
- Latency is acceptable for conversation
- Errors handled without crashing

---

## Notes
- Voice pipeline is complex - test each component separately
- Latency is critical for natural conversation
- Consider caching TTS for common responses
- Audio normalization improves consistency
- Noise gate reduces false VAD triggers
- Next modules will add frontend (MODULE-4) to complete the system
- Monitor memory usage with long conversations
- Consider speech enhancement (noise reduction, echo cancellation) for production
