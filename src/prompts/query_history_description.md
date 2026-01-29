# 🔍 Query History Tool

## Tool Name
`query_history`

## Description
Queries the saved transcription history. You can search for specific text or view the latest transcriptions. Useful for reviewing previous work or finding specific content.

## Parameters
- **search** (optional): Text to search in transcriptions. If not specified, shows all
- **limit** (optional): Maximum number of results to display (default: 10, max: 100)

## Usage Examples
- "Show me the last 5 transcriptions"
- "Search for transcriptions containing 'project management'"
- "Find all mentions of 'artificial intelligence' in history"
- "Query the transcription database"
- "What have we transcribed recently?"
- "Search history for 'meeting notes'"

## When to Use
- User wants to see previous transcriptions
- User asks to search for specific content in history
- User wants to review past work
- User mentions "history", "previous", "past", "before"
- User wants to find specific information from transcribed content
- User asks what files have been processed

## Notes
- Returns transcriptions in reverse chronological order (newest first)
- Shows timestamp, filename, duration, model, and text preview
- Search is case-insensitive and looks within transcription text
- Limited results prevent overwhelming output
- Useful for finding specific quotes or topics from past sessions