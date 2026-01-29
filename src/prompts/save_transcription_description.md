# 💾 Save Transcription Tool

## Tool Name
`save_transcription`

## Description
Saves a transcription to the CSV history. Requires the filename, transcribed text, the model used, and optionally the audio duration.

## Parameters
- **filename** (required): Name of the transcribed audio file
- **text** (required): Transcribed text content
- **model** (optional): Model used for transcription (default: "whisper-base")
- **duration** (optional): Audio duration in seconds

## Usage Examples
- "Save this transcription with filename podcast.mp3 and text [content]"
- "Store the transcription in history"
- "Add this to the transcription database"
- "Save the results to CSV"

## When to Use
- After completing a transcription that needs to be stored
- User wants to save transcription results permanently
- Need to maintain a record of transcribed content
- User asks to save, store, or add to history/database

## Notes
- Automatically adds timestamp when saving
- Maintains CSV format for easy access and export
- Returns confirmation with total count of transcriptions
- Useful for building a searchable archive of transcriptions