"""
API REST Server for Audio Transcription
=====================================

FastAPI server that provides endpoints for:
- Upload and transcribe audio files
- Query transcription history
- Download transcriptions as CSV

Author: AI Transcription System
"""

import os
import io
import csv
from datetime import datetime
from pathlib import Path
from typing import Optional, List

import pandas as pd
import requests
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Response, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from dotenv import load_dotenv

# Import agent
from src.agent import create_agent

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Audio Transcription API",
    description="API for transcribing audio files using Deepgram",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration from .env file
UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/app/data/audio/uploads"))
TRANSCRIPTIONS_DIR = Path(os.getenv("TRANSCRIPTIONS_DIR", "/app/data/transcriptions"))
CSV_PATH = Path(os.getenv("CSV_PATH", "/app/data/transcriptions/output/history.csv"))
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

# Ensure directories exist
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

# Initialize agent
try:
    agent = create_agent()
    print("✅ Agent initialized successfully")
except Exception as e:
    print(f"⚠️ Warning: Could not initialize agent: {e}")
    agent = None

# Initialize CSV if it doesn't exist
def initialize_csv():
    if not CSV_PATH.exists():
        df = pd.DataFrame(columns=[
            'timestamp',
            'filename',
            'duration_seconds',
            'model',
            'transcription_text'
        ])
        df.to_csv(CSV_PATH, index=False, encoding='utf-8')

initialize_csv()

# Pydantic models
class AgentRequest(BaseModel):
    message: str
    file: Optional[str] = None  # Optional file path if message references a file

class AgentResponse(BaseModel):
    success: bool
    message: str
    response: str
    action_taken: Optional[str] = None
    data: Optional[dict] = None



class TranscriptionResponse(BaseModel):
    success: bool
    message: str
    filename: str
    transcription: Optional[str] = None
    duration: Optional[float] = None
    timestamp: Optional[str] = None

class HistoryItem(BaseModel):
    timestamp: str
    filename: str
    duration_seconds: Optional[float] = None
    model: str
    transcription_text: str

class HistoryResponse(BaseModel):
    success: bool
    total_count: int
    transcriptions: List[HistoryItem]

# Helper functions
def save_to_csv(filename: str, transcription: str, duration: float, model: str = "deepgram-nova-2") -> str:
    """Save transcription to CSV history."""
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        
        new_row = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'filename': filename,
            'duration_seconds': duration,
            'model': model,
            'transcription_text': transcription
        }
        
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(CSV_PATH, index=False, encoding='utf-8')
        
        return str(len(df))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving to CSV: {str(e)}")

def transcribe_audio(audio_file_path: Path, language: str = "es") -> tuple[str, float]:
    """Transcribe audio file using Deepgram API."""
    if not DEEPGRAM_API_KEY:
        raise HTTPException(status_code=500, detail="DEEPGRAM_API_KEY not configured")
    
    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": "audio/*"
    }
    
    start_time = datetime.now()
    
    with open(audio_file_path, 'rb') as f:
        response = requests.post(
            f"https://api.deepgram.com/v1/listen?model=nova-2&language={language}",
            headers=headers,
            data=f
        )
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    if response.status_code != 200:
        raise HTTPException(
            status_code=500, 
            detail=f"Deepgram API error: {response.status_code} - {response.text}"
        )
    
    result = response.json()
    transcription = result.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '').strip()
    
    if not transcription:
        raise HTTPException(status_code=500, detail="No transcription received from API")
    
    return transcription, duration

# API Endpoints
@app.get("/", status_code=200)
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Audio Transcription API",
        "version": "1.0.0",
        "endpoints": {
            "agent": "/agent - Intelligent endpoint that decides what action to take based on your message",
            "upload": "/upload - Legacy direct transcription endpoint",
            "history": "/history - Direct history query",
            "download": "/download - Download CSV history",
            "health": "/health - Health check"
        }
    }

@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_key_configured": bool(DEEPGRAM_API_KEY)
    }

@app.post("/agent")
async def agent_process(
    message: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    """Intelligent agent that decides what action to take based on the message content using function calling."""

    saved_file_path = None

    try:
        # Build the full message
        full_message = message

        # Handle file upload if provided
        if file and file.filename:
            # Validate file
            valid_extensions = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.mp4'}
            file_ext = Path(file.filename).suffix.lower()

            if file_ext not in valid_extensions:
                return f"Error: Extensión de archivo no válida. Formatos soportados: {', '.join(valid_extensions)}"

            # Save uploaded file
            file_path = UPLOAD_DIR / file.filename
            content = await file.read()

            with open(file_path, "wb") as f:
                f.write(content)

            saved_file_path = str(file_path)

            # Add file info to message
            full_message = f"{message}. Archivo subido: {saved_file_path}"

        # Use intelligent agent if available
        if agent is not None:
            try:
                # Invoke agent with message
                result = agent.invoke({
                    "messages": [{"role": "user", "content": full_message}]
                })

                # Extract response
                if "messages" in result and len(result["messages"]) > 0:
                    response_text = result["messages"][-1]["content"]
                else:
                    response_text = str(result)

                return response_text

            except Exception as agent_error:
                # If agent fails, fall back to simple logic
                print(f"Agent error: {agent_error}")
                return f"Error del agente inteligente: {str(agent_error)}"

        # Fallback: Simple keyword-based logic if agent not available
        message_lower = full_message.lower()

        if any(word in message_lower for word in ["historial", "historico", "history", "consultar", "buscar"]):
            try:
                df = pd.read_csv(CSV_PATH, encoding='utf-8')
                if len(df) == 0:
                    response_text = "No hay transcripciones en el historial aún."
                else:
                    recent = df.sort_values('timestamp', ascending=False).head(5)
                    response_text = "Historial de transcripciones recientes:\n\n"
                    for _, row in recent.iterrows():
                        response_text += f"📄 {row['filename']}\n"
                        response_text += f"📅 {row['timestamp']}\n"
                        response_text += f"📝 {row['transcription_text'][:100]}...\n\n"
            except Exception as e:
                response_text = f"Error al consultar el historial: {str(e)}"

        elif "transcrib" in message_lower and saved_file_path:
            try:
                transcription, duration = transcribe_audio(Path(saved_file_path), "es")
                save_to_csv(Path(saved_file_path).name, transcription, duration)
                response_text = f"Transcripción completada:\n\nArchivo: {Path(saved_file_path).name}\nDuración: {duration:.2f} segundos\n\nTranscripción:\n{transcription}"
            except Exception as e:
                response_text = f"Error al transcribir el archivo: {str(e)}"

        else:
            response_text = "Puedo ayudarte a:\n- Transcribir archivos de audio (adjunta un archivo y menciona 'transcribir')\n- Consultar el historial de transcripciones (menciona 'historial' o 'consultar')"

        return response_text

    except Exception as e:
        # Clean up uploaded file on error
        if saved_file_path and Path(saved_file_path).exists():
            Path(saved_file_path).unlink()
        return f"Error durante el procesamiento: {str(e)}"

@app.post("/upload", response_model=TranscriptionResponse)
async def upload_and_transcribe(
    file: UploadFile = File(...),
    language: str = Query(default="es", description="Language code (es, en, etc.)")
):
    """Legacy endpoint for direct audio upload and transcription."""
    
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    valid_extensions = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.mp4'}
    file_ext = Path(file.filename).suffix.lower()
    
    if file_ext not in valid_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file extension. Supported: {', '.join(valid_extensions)}"
        )
    
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Transcribe
        transcription, duration = transcribe_audio(file_path, language)
        
        # Save to history
        total_count = save_to_csv(file.filename, transcription, duration)
        
        return TranscriptionResponse(
            success=True,
            message="File transcribed successfully",
            filename=file.filename,
            transcription=transcription,
            duration=duration,
            timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/history", response_model=HistoryResponse)
async def get_history(
    search: Optional[str] = Query(None, description="Search term in transcriptions"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of results")
):
    """Get transcription history."""
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        
        if len(df) == 0:
            return HistoryResponse(success=True, total_count=0, transcriptions=[])
        
        # Filter by search term if provided
        if search:
            mask = df['transcription_text'].str.contains(search, case=False, na=False)
            df = df[mask]
        
        # Sort by timestamp (newest first) and limit
        df = df.sort_values('timestamp', ascending=False).head(limit)
        
        transcriptions = []
        for _, row in df.iterrows():
            transcriptions.append(HistoryItem(
                timestamp=row['timestamp'],
                filename=row['filename'],
                duration_seconds=row['duration_seconds'] if pd.notna(row['duration_seconds']) else None,
                model=row['model'],
                transcription_text=row['transcription_text']
            ))
        
        return HistoryResponse(
            success=True,
            total_count=len(transcriptions),
            transcriptions=transcriptions
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading history: {str(e)}")

@app.get("/download")
async def download_csv():
    """Download transcription history as CSV file."""
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        
        if len(df) == 0:
            raise HTTPException(status_code=404, detail="No transcriptions found")
        
        # Create CSV in memory
        output = io.StringIO()
        df.to_csv(output, index=False, encoding='utf-8')
        output.seek(0)
        
        # Create response
        response = Response(
            content=output.getvalue(),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=transcriptions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            }
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating CSV: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get transcription statistics."""
    try:
        df = pd.read_csv(CSV_PATH, encoding='utf-8')
        
        if len(df) == 0:
            return {
                "total_transcriptions": 0,
                "total_duration_seconds": 0,
                "average_duration_seconds": 0,
                "most_used_model": None,
                "recent_files": []
            }
        
        total_transcriptions = len(df)
        total_duration = df['duration_seconds'].sum()
        avg_duration = df['duration_seconds'].mean()
        most_used_model = df['model'].mode().iloc[0] if not df['model'].mode().empty else None
        recent_files = df.sort_values('timestamp', ascending=False).head(5)['filename'].tolist()
        
        return {
            "total_transcriptions": total_transcriptions,
            "total_duration_seconds": round(total_duration, 2),
            "average_duration_seconds": round(avg_duration, 2),
            "most_used_model": most_used_model,
            "recent_files": recent_files
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating stats: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)