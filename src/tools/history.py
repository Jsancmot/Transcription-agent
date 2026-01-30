"""Tool for managing transcription history in CSV format."""

import os
import csv
from typing import Type, Optional, List
from datetime import datetime
from pathlib import Path

import pandas as pd
from langchain.tools import BaseTool
from pydantic import BaseModel, Field


class SaveTranscriptionInput(BaseModel):
    """Input schema for saving a transcription to history."""

    filename: str = Field(description="Name of the transcribed audio file")
    text: str = Field(description="Transcribed text")
    model: str = Field(default="whisper-base", description="Model used for transcription")
    duration: Optional[float] = Field(default=None, description="Audio duration in seconds")


class QueryHistoryInput(BaseModel):
    """Input schema for querying transcription history."""

    search: Optional[str] = Field(
        default=None,
        description="Text to search in transcriptions. If not specified, shows all"
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results to display (must be an integer number, e.g., 5, 10, 20)"
    )


class HistoryTool(BaseTool):
    """Tool for managing transcription history."""

    name: str = "manage_history"
    description: str = (
        "Manages the transcription history in a CSV file. "
        "Can save new transcriptions or query the history. "
        "Available actions: 'save' or 'query'. "
        "To save: provide filename, text, model, and optionally duration. "
        "To query: optionally provide a search term and result limit."
    )

    csv_path: str = Field(default="data/transcriptions/output/history.csv")

    def __init__(self, csv_path: str = "data/transcriptions/output/history.csv"):
        super().__init__()
        self.csv_path = csv_path
        self._initialize_csv()

    def _initialize_csv(self):
        """Creates the CSV file with headers if it doesn't exist."""
        csv_file = Path(self.csv_path)
        csv_file.parent.mkdir(parents=True, exist_ok=True)

        if not csv_file.exists():
            df = pd.DataFrame(columns=[
                'timestamp',
                'filename',
                'duration_seconds',
                'model',
                'transcription_text'
            ])
            df.to_csv(self.csv_path, index=False, encoding='utf-8')

    def save_transcription(
        self,
        filename: str,
        text: str,
        model: str = "whisper-base",
        duration: Optional[float] = None
    ) -> str:
        """Saves a new transcription to the CSV."""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_row = {
                'timestamp': timestamp,
                'filename': filename,
                'duration_seconds': duration if duration else '',
                'model': model,
                'transcription_text': text
            }

            # Read existing CSV
            df = pd.read_csv(self.csv_path, encoding='utf-8')

            # Add new row
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # Save
            df.to_csv(self.csv_path, index=False, encoding='utf-8')

            total_transcriptions = len(df)
            return (
                f"Transcription saved successfully to history.\n"
                f"Timestamp: {timestamp}\n"
                f"Total transcriptions in history: {total_transcriptions}"
            )

        except Exception as e:
            return f"Error saving transcription: {str(e)}"

    def query_history(
        self,
        search: Optional[str] = None,
        limit: int = 10
    ) -> str:
        """Queries the transcription history."""
        try:
            df = pd.read_csv(self.csv_path, encoding='utf-8')

            if len(df) == 0:
                return "History is empty. No transcriptions saved."

            # Filter if search term provided
            if search:
                mask = df['transcription_text'].str.contains(
                    search,
                    case=False,
                    na=False
                )
                df = df[mask]

                if len(df) == 0:
                    return f"No transcriptions found containing '{search}'."

            # Limit results
            df = df.tail(limit)

            # Format results
            result = f"Transcription history (showing last {len(df)}):\n\n"

            for idx, row in df.iterrows():
                duration_str = f"{row['duration_seconds']:.1f}s" if pd.notna(row['duration_seconds']) else "N/A"
                text_preview = row['transcription_text'][:100] + "..." if len(row['transcription_text']) > 100 else row['transcription_text']

                result += f"""
{'='*60}
Date: {row['timestamp']}
File: {row['filename']}
Duration: {duration_str}
Model: {row['model']}
Text: {text_preview}
"""

            result += f"\n{'='*60}\n"
            result += f"Total transcriptions found: {len(df)}"

            return result

        except Exception as e:
            return f"Error querying history: {str(e)}"

    def _run(self, query: str) -> str:
        """
        Executes the tool. Expects a string with format:
        'action: save/query, parameters...'

        Note: This is a simplified implementation. In production,
        consider using args_schema with Union types or separate tools.
        """
        # This tool can be improved by creating two separate tools
        # For now, we parse the query manually

        if "save" in query.lower():
            return "To save, call the save_transcription method directly from code."
        else:
            # Default to query
            return self.query_history()

    async def _arun(self, *args, **kwargs) -> str:
        """Asynchronous version."""
        return self._run(*args, **kwargs)


# Specific tools for better agent integration
class SaveTranscriptionTool(BaseTool):
    """Specific tool for saving transcriptions."""

    name: str = "save_transcription"
    description: str = (
        "Saves a transcription to the CSV history. "
        "Requires the filename, transcribed text, "
        "the model used, and optionally the audio duration."
    )
    args_schema: Type[BaseModel] = SaveTranscriptionInput

    def __init__(self, **kwargs):
        """Initialize the tool with history instance."""
        super().__init__(**kwargs)
        self.history = HistoryTool()

    def _run(
        self,
        filename: str,
        text: str,
        model: str = "whisper-base",
        duration: Optional[float] = None
    ) -> str:
        return self.history.save_transcription(filename, text, model, duration)

    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)


class QueryHistoryTool(BaseTool):
    """Specific tool for querying history."""

    name: str = "query_history"
    description: str = (
        "Queries the saved transcription history. "
        "You can search for specific text or view the latest transcriptions. "
        "Useful for reviewing previous work or finding specific content."
    )
    args_schema: Type[BaseModel] = QueryHistoryInput

    def __init__(self, **kwargs):
        """Initialize the tool with history instance."""
        super().__init__(**kwargs)
        self.history = HistoryTool()

    def _run(
        self,
        search: Optional[str] = None,
        limit: int = 10
    ) -> str:
        return self.history.query_history(search, limit)

    async def _arun(self, *args, **kwargs) -> str:
        return self._run(*args, **kwargs)
