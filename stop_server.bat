@echo off
echo Stopping Transcription API Server...
echo.

docker stop transcription-api-server >nul 2>&1
docker rm transcription-api-server >nul 2>&1

echo Server stopped successfully!
echo.
echo ================================
echo  API Server stopped!
echo ================================
pause