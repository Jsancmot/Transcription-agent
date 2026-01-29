#!/bin/bash

# Evitar que Git Bash traduzca mal las rutas en Windows (causante de carpetas como transcriptions;C)
export MSYS_NO_PATHCONV=1

# Get current directory
PROJECT_DIR=$(pwd)

# Define paths using current directory
UPLOAD_DIR="${PROJECT_DIR}/data/audio/uploads"
TRANSCRIPTIONS_DIR="${PROJECT_DIR}/data/transcriptions"

echo "Starting Transcription API Server..."
echo "Project Directory: $PROJECT_DIR"
echo "Upload Directory: $UPLOAD_DIR"
echo "Transcriptions Directory: $TRANSCRIPTIONS_DIR"
echo ""

# Stop existing container if running
docker stop transcription-api-server 2>/dev/null
docker rm transcription-api-server 2>/dev/null

# Start new container with automatic path mounting
docker run -d -p 8000:8000 \
    --env-file .env \
    -v "${UPLOAD_DIR}:/app/data/audio/uploads" \
    -v "${TRANSCRIPTIONS_DIR}:/app/data/transcriptions" \
    --name transcription-api-server \
    transcription-api

echo ""
echo "Server starting up..."
sleep 3

echo "Testing API..."
curl -X GET http://localhost:8000/health

echo ""
echo "================================"
echo " API Server is running!"
echo " URL: http://localhost:8000"
echo " Docs: http://localhost:8000/docs"
echo "================================"