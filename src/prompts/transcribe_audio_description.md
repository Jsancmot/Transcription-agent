# 🎧 Audio Transcription Tool

## Tool Name
`transcribe_audio`

## Description
Transcribes an audio file to text using Deepgram API. Useful for converting voice recordings, podcasts, interviews, etc. to text. Accepts formats: mp3, wav, m4a, ogg, flac. Use this tool when the user asks to transcribe or convert audio to text.

## Parameters
- **audio_file** (required): Full path to the audio file to transcribe. Supported formats: mp3, wav, m4a, ogg, flac
- **model** (optional): Whisper model to use. Options: tiny, base, small, medium, large. Base is recommended for speed/accuracy balance
- **language** (optional): Language code (e.g., 'es' for Spanish, 'en' for English). If not specified, language will be auto-detected

## Usage Examples
- "Transcribe the file /path/to/audio.mp3"
- "Convert the podcast episode to text using the small model"
- "Transcribe interview.wav in Spanish"
- "I need to transcribe this audio file: meeting.m4a"

## When to Use
- User wants to convert audio to text
- User mentions transcribing, converting, or extracting text from audio
- User provides an audio file path and wants the content
- User asks for speech-to-text functionality

## Notes
- The tool automatically validates file existence and format
- Supports multiple audio formats
- Can detect language automatically or use specified language
- Returns processing time and model information along with transcription