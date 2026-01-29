"""Tool for transcribing audio files using Deepgram API."""

import os
from typing import Type, Optional
from datetime import datetime
from pathlib import Path

from langchain.tools import BaseTool
from pydantic import BaseModel, Field

import requests


class TranscribeAudioInput(BaseModel):
    """Input schema for the transcription tool."""

    audio_file: str = Field(
        description="Full path to the audio file to transcribe. "
                    "Supported formats: mp3, wav, m4a, ogg, flac"
    )
    model: str = Field(
        default="nova-2",
        description="Deepgram model to use. Options: nova-2 (recommended), base, enhanced."
    )
    language: Optional[str] = Field(
        default=None,
        description="Language code (e.g., 'es' for Spanish, 'en' for English). "
                    "If not specified, language will be auto-detected"
    )



class TranscribeAudioTool(BaseTool):
    """Tool for transcribing audio files using Deepgram API."""

    name: str = "transcribe_audio"
    description: str = (
        "Transcribes an audio file to text using Deepgram API. "
        "Useful for converting voice recordings, podcasts, interviews, etc. to text. "
        "Accepts formats: mp3, wav, m4a, ogg, flac. "
        "Use this tool when the user asks to transcribe or convert audio to text."
    )
    args_schema: Type[BaseModel] = TranscribeAudioInput

    def _run(
        self,
        audio_file: str,
        model: str = "nova-2",
        language: Optional[str] = None
    ) -> str:
        """Executes the audio file transcription using Deepgram API."""

        # Validate that the file exists
        audio_path = Path(audio_file)
        if not audio_path.exists():
            return f"Error: The file '{audio_file}' does not exist."

        # Validate file extension
        valid_extensions = {'.mp3', '.wav', '.m4a', '.ogg', '.flac', '.mp4'}
        if audio_path.suffix.lower() not in valid_extensions:
            return (
                f"Error: Unsupported file format '{audio_path.suffix}'. "
                f"Valid formats: {', '.join(valid_extensions)}"
            )

        # Validate model
        valid_models = ['nova-2', 'nova', 'base', 'enhanced']
        if model not in valid_models:
            return (
                f"Error: Invalid model '{model}'. "
                f"Available Deepgram models: {', '.join(valid_models)}"
            )

        try:
            return self._transcribe_with_deepgram(audio_path, model, language)
        except Exception as e:
            return f"Error during transcription: {str(e)}"

    def _transcribe_with_deepgram(self, audio_path: Path, model: str, language: Optional[str]) -> str:
        """Transcribe using Deepgram API."""
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("DEEPGRAM_API_KEY")
        if not api_key:
            return "Error: DEEPGRAM_API_KEY not configured in environment variables."

        print(f"Transcribing '{audio_path.name}' with Deepgram API (model: {model})...")

        headers = {
            "Authorization": f"Token {api_key}",
            "Content-Type": "audio/*"
        }

        # Configure language for Deepgram
        language_code = language if language else "auto"

        start_time = datetime.now()
        with open(audio_path, 'rb') as audio_file:
            response = requests.post(
                f"https://api.deepgram.com/v1/listen?model={model}&language={language_code}",
                headers=headers,
                data=audio_file
            )
        end_time = datetime.now()

        if response.status_code != 200:
            return f"Error from Deepgram API: {response.status_code} - {response.text}"

        result = response.json()
        processing_duration = (end_time - start_time).total_seconds()

        # Extract transcript from Deepgram response
        try:
            text = result.get('results', {}).get('channels', [{}])[0].get('alternatives', [{}])[0].get('transcript', '').strip()
            detected_language = language_code if language != "auto" else "auto-detected"
        except (IndexError, KeyError):
            return "Error parsing Deepgram API response"

        return self._format_response(audio_path.name, f'deepgram-{model}', detected_language, processing_duration, text)

    def _format_response(self, filename: str, model: str, language: str, duration: float, text: str) -> str:
        """Format the transcription response."""
        return f"""Transcription completed successfully:

File: {filename}
Model used: {model}
Detected language: {language}
Processing time: {duration:.2f} seconds

Transcribed text:
{text}
"""

    async def _arun(self, *args, **kwargs) -> str:
        """Asynchronous version (not implemented, uses synchronous version)."""
        return self._run(*args, **kwargs)
