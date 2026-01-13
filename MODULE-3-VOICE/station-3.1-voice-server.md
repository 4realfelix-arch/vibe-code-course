# Station 3.1 - Voice Server Setup

## Overview
Set up the Python voice processing server that handles Speech-to-Text (STT) and Text-to-Speech (TTS) using the LFM2.5-Audio-1.5B model. This server runs on GPU-equipped Server 2 and provides voice capabilities via WebSocket.

## Learning Objectives
- Build PyTorch-based voice processing server
- Load and use LFM2.5-Audio-1.5B model
- Handle audio streaming with WebSockets
- Implement GPU acceleration for voice models
- Manage audio format conversion

---

## 🎯 GENERATION PROMPT

Create a voice processing server for Atomic Cat AI using LFM2.5-Audio-1.5B:

**File: voice-server/server.py**

```python
import asyncio
import json
import logging
import torch
import torchaudio
from pathlib import Path
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Optional
import numpy as np

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
MODEL_PATH = Path(os.getenv("MODEL_PATH", "/models/lfm2.5-audio-1.5b"))
GPU_ENABLED = os.getenv("GPU_ENABLED", "true").lower() == "true"
DEVICE = "cuda" if GPU_ENABLED and torch.cuda.is_available() else "cpu"
SAMPLE_RATE = 16000  # 16kHz for voice

app = FastAPI(
    title="Atomic Cat Voice Server",
    description="Voice processing with LFM2.5-Audio-1.5B",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceModel:
    """Wrapper for LFM2.5-Audio-1.5B model"""
    
    def __init__(self, model_path: Path, device: str):
        self.device = device
        self.model = None
        self.model_path = model_path
        self.loaded = False
        
    def load(self):
        """Load model into memory"""
        if self.loaded:
            return
        
        try:
            logger.info(f"Loading model from {self.model_path} on {self.device}")
            
            # TODO: Replace with actual LFM2.5 loading
            # This is a placeholder - actual implementation depends on model format
            # from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
            # self.processor = AutoProcessor.from_pretrained(str(self.model_path))
            # self.model = AutoModelForSpeechSeq2Seq.from_pretrained(
            #     str(self.model_path),
            #     torch_dtype=torch.float16 if self.device == "cuda" else torch.float32
            # ).to(self.device)
            
            self.loaded = True
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def transcribe(self, audio_data: np.ndarray) -> str:
        """
        Convert speech to text
        
        Args:
            audio_data: Audio samples as numpy array (16kHz)
        
        Returns:
            Transcribed text
        """
        if not self.loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            # Convert numpy to tensor
            audio_tensor = torch.from_numpy(audio_data).float()
            if self.device == "cuda":
                audio_tensor = audio_tensor.cuda()
            
            # Transcribe
            with torch.no_grad():
                # TODO: Replace with actual LFM2.5 inference
                # result = self.model.generate(audio_tensor)
                # text = self.processor.decode(result[0])
                
                # Placeholder
                text = "[Transcription placeholder - implement LFM2.5 inference]"
            
            return text
        except Exception as e:
            logger.error(f"Transcription failed: {e}")
            raise
    
    def synthesize(self, text: str) -> bytes:
        """
        Convert text to speech
        
        Args:
            text: Text to synthesize
        
        Returns:
            Audio bytes (WAV format, 16kHz)
        """
        if not self.loaded:
            raise RuntimeError("Model not loaded")
        
        try:
            with torch.no_grad():
                # TODO: Replace with actual LFM2.5 TTS inference
                # audio_tensor = self.model.synthesize(text)
                
                # Placeholder: Generate silence
                duration = len(text.split()) * 0.5  # ~0.5s per word
                samples = int(SAMPLE_RATE * duration)
                audio_tensor = torch.zeros(samples)
            
            # Convert to bytes (WAV format)
            audio_bytes = audio_tensor_to_wav(audio_tensor, SAMPLE_RATE)
            return audio_bytes
        except Exception as e:
            logger.error(f"Synthesis failed: {e}")
            raise

def audio_tensor_to_wav(tensor: torch.Tensor, sample_rate: int) -> bytes:
    """Convert audio tensor to WAV bytes"""
    import io
    buffer = io.BytesIO()
    torchaudio.save(buffer, tensor.unsqueeze(0), sample_rate, format="wav")
    return buffer.getvalue()

def bytes_to_audio_array(audio_bytes: bytes) -> np.ndarray:
    """Convert audio bytes to numpy array"""
    import io
    buffer = io.BytesIO(audio_bytes)
    audio, sr = torchaudio.load(buffer)
    
    # Resample if needed
    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        audio = resampler(audio)
    
    # Convert to mono if stereo
    if audio.shape[0] > 1:
        audio = torch.mean(audio, dim=0)
    
    return audio.squeeze().numpy()

# Initialize model
voice_model = VoiceModel(MODEL_PATH, DEVICE)

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    try:
        voice_model.load()
        logger.info("Voice server ready")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        # Continue anyway for development

@app.get("/")
async def root():
    """Health check"""
    return {
        "service": "Atomic Cat Voice Server",
        "status": "operational",
        "model_loaded": voice_model.loaded,
        "device": DEVICE
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy" if voice_model.loaded else "degraded",
        "model_loaded": voice_model.loaded,
        "device": DEVICE,
        "gpu_available": torch.cuda.is_available(),
        "sample_rate": SAMPLE_RATE
    }

@app.post("/transcribe")
async def transcribe_audio(audio_data: bytes):
    """
    Transcribe audio to text
    
    Expects raw audio bytes (WAV format preferred)
    """
    try:
        audio_array = bytes_to_audio_array(audio_data)
        text = voice_model.transcribe(audio_array)
        return {"text": text, "success": True}
    except Exception as e:
        logger.error(f"Transcription endpoint error: {e}")
        return {"error": str(e), "success": False}

@app.post("/synthesize")
async def synthesize_speech(text: str):
    """
    Synthesize speech from text
    
    Returns WAV audio bytes
    """
    try:
        audio_bytes = voice_model.synthesize(text)
        return audio_bytes
    except Exception as e:
        logger.error(f"Synthesis endpoint error: {e}")
        return {"error": str(e), "success": False}

if __name__ == "__main__":
    import os
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8765)),
        log_level="info"
    )
```

**File: voice-server/requirements.txt**
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
torch==2.1.2
torchaudio==2.1.2
numpy==1.26.3
websockets==12.0
```

**File: voice-server/Dockerfile**
```dockerfile
FROM pytorch/pytorch:2.1.2-cuda12.1-cudnn8-runtime

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8765

# Run server
CMD ["python", "server.py"]
```

**Requirements**:
1. Use PyTorch for model inference
2. Support GPU acceleration via CUDA
3. Handle 16kHz audio (standard for voice)
4. Provide both HTTP endpoints and health checks
5. Include placeholder for LFM2.5 model loading (actual implementation depends on model format)
6. Convert between audio formats (bytes, tensor, numpy)
7. Log all operations
8. Handle errors gracefully

**Output**: Complete voice server with STT/TTS placeholders ready for LFM2.5 integration.

---

## ✅ VALIDATION PROMPT

Validate voice server setup:

### File Structure
- [ ] `voice-server/server.py` exists
- [ ] `voice-server/requirements.txt` exists
- [ ] `voice-server/Dockerfile` exists

### Model Configuration
- [ ] Reads `MODEL_PATH` from environment
- [ ] Reads `GPU_ENABLED` from environment
- [ ] Detects CUDA availability
- [ ] Uses appropriate device (cuda/cpu)
- [ ] Configures 16kHz sample rate

### VoiceModel Class
- [ ] Has `load()` method for model initialization
- [ ] Has `transcribe()` method (STT)
- [ ] Has `synthesize()` method (TTS)
- [ ] Tracks loaded state
- [ ] Handles GPU tensors correctly
- [ ] Includes placeholder comments for LFM2.5 integration

### Audio Processing Functions
- [ ] `audio_tensor_to_wav()` converts tensor to WAV bytes
- [ ] `bytes_to_audio_array()` converts bytes to numpy array
- [ ] Handles resampling to 16kHz
- [ ] Converts stereo to mono
- [ ] Uses torchaudio for audio operations

### API Endpoints
- [ ] **GET /** returns service info
- [ ] **GET /health** returns detailed health status
- [ ] **POST /transcribe** accepts audio bytes, returns text
- [ ] **POST /synthesize** accepts text, returns audio bytes
- [ ] All endpoints handle errors gracefully

### Dockerfile
- [ ] Uses PyTorch CUDA base image
- [ ] Installs audio dependencies (libsndfile1, ffmpeg)
- [ ] Installs Python requirements
- [ ] Exposes port 8765
- [ ] Runs server.py

### Commands to Run
```bash
cd voice-server

# Build Docker image
docker build -t atomic-cat-voice:test .

# Should complete without errors

# Run server (CPU mode for testing)
docker run -p 8765:8765 \
  -e GPU_ENABLED=false \
  -e MODEL_PATH=/models/placeholder \
  atomic-cat-voice:test

# In another terminal, test endpoints:

# Health check
curl http://localhost:8765/health | jq .
# Should show status, model_loaded, device

# Root endpoint
curl http://localhost:8765/ | jq .
# Should show service info

# Note: transcribe/synthesize will use placeholders until LFM2.5 integrated
```

### Expected Results
- Server starts without errors
- Health check returns status
- GPU detection works correctly
- Audio processing functions compile
- Ready for LFM2.5 model integration
- Next station will add WebSocket for real-time streaming

---

## Notes
- LFM2.5-Audio-1.5B model format may vary - adjust loading code accordingly
- Model files are large (~3GB) - download separately
- GPU significantly speeds up inference (10-50x faster)
- WebSocket streaming (station 3.2) will be more efficient than HTTP
- Consider model quantization for faster inference
- Next station adds real-time voice with barge-in support
