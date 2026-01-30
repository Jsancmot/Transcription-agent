"""
Test script for individual tools
Without needing to use the complete agent
"""

import os
import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.tools.transcriber import TranscribeAudioTool
from src.tools.history import SaveTranscriptionTool, QueryHistoryTool

# Check if running in CI environment
IS_CI = os.getenv('CI', 'false').lower() == 'true' or os.getenv('GITHUB_ACTIONS', 'false').lower() == 'true'


def test_transcription():
    """Tests the transcription tool."""
    print("="*70)
    print("TEST: Transcription Tool")
    print("="*70)

    # Skip in CI environment
    if IS_CI:
        print("\n⏭️  Skipping transcription test in CI environment")
        print("   (requires audio files and API keys)")
        return

    # Check if there are sample audio files
    audio_dir = Path("audio_samples")
    if not audio_dir.exists() or not list(audio_dir.glob("*")):
        print("\n⚠️  No audio files found in 'audio_samples/'")
        print("\nTo test transcription:")
        print("1. Create the 'audio_samples' folder")
        print("2. Place an audio file (mp3, wav, etc.)")
        print("3. Run this script again")
        return

    # Search for first audio file
    formats = ['*.mp3', '*.wav', '*.m4a', '*.ogg', '*.flac']
    audio_file = None

    for format in formats:
        files = list(audio_dir.glob(format))
        if files:
            audio_file = str(files[0])
            break

    if not audio_file:
        print("No compatible audio files found.")
        return

    print(f"\n📁 Test file: {audio_file}")
    print("\n⏳ Transcribing (this may take a few seconds)...\n")

    tool = TranscribeAudioTool()
    result = tool._run(
        audio_file=audio_file,
        model="base",
        language="en"
    )

    print(result)


def test_history():
    """Tests the history tools."""
    print("\n" + "="*70)
    print("TEST: History Tools")
    print("="*70)

    # Save a test transcription
    print("\n1️⃣ Saving test transcription...")
    save_tool = SaveTranscriptionTool()
    result = save_tool._run(
        filename="test_audio.mp3",
        text="This is a test transcription to verify that the system works correctly.",
        model="whisper-base",
        duration=30.5
    )
    print(result)

    # Query the history
    print("\n2️⃣ Querying history...")
    query_tool = QueryHistoryTool()
    result = query_tool._run(limit=5)
    print(result)

    # Search in history
    print("\n3️⃣ Searching for 'test' in history...")
    result = query_tool._run(search="test", limit=5)
    print(result)


def main():
    """Main function."""
    print("\n" + "🧪"*35)
    print("  TOOLS TEST SCRIPT")
    print("🧪"*35 + "\n")

    if IS_CI:
        print("Running in CI environment - some tests will be skipped\n")

    # Test history tools (always work)
    try:
        test_history()
    except Exception as e:
        print(f"\n❌ History tests failed: {e}")
        sys.exit(1)

    # Test transcription (requires audio file)
    try:
        test_transcription()
    except Exception as e:
        print(f"\n❌ Transcription tests failed: {e}")
        if not IS_CI:  # Only fail in local environment
            sys.exit(1)

    print("\n" + "="*70)
    print("✅ Tests completed successfully")
    print("="*70)

    if not IS_CI:
        print("\nIf everything worked correctly, the main agent should work.")
        print("Run: python agent.py")

    sys.exit(0)


if __name__ == "__main__":
    main()
