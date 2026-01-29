@echo off
echo Starting Transcription API Server...
echo.

REM Stop existing container if running
docker stop transcription-agent >nul 2>&1
docker rm transcription-agent >nul 2>&1

REM Start new container with automatic path mounting using current directory
docker run -d -p 8000:8000 --env-file .env -v "%CD%\data\audio\uploads":/app/data/audio/uploads -v "%CD%\data\transcriptions":/app/data/transcriptions --name transcription-agent transcription-agent

echo.
echo Server starting up...
timeout /t 3 >nul

echo Testing API...
curl -X GET http://localhost:8000/health

echo.
echo ================================
echo  API Server is running!
echo  URL: http://localhost:8000
echo  Docs: http://localhost:8000/docs
echo ================================
pause