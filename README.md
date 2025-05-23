# YouTube Transcript MCP

A Python-based MCP (Model Control Protocol) server that provides a robust solution for extracting transcripts from YouTube videos using both subtitle-based and audio-based transcription methods. This project enables AI assistants to easily obtain transcripts from any YouTube video through a standardized interface.

## Table of Contents
* [What It Does](#what-it-does)
* [Project Architecture](#project-architecture)
* [Quick Started](#quick-started)
* [Usage](#usage)

## What It Does

This MCP server provides a dual-approach transcription system:

### Primary Method: Subtitle-based Transcription
- Extracts available subtitles from YouTube videos
- Supports multiple language preferences
- Uses the `youtube_transcript_api` for efficient subtitle extraction

### Fallback Method: Audio-based Transcription
If subtitles are unavailable or explicitly requested, the system will:
- Download the video's audio track using `pytubefix`
- Convert the audio to a suitable format using `pydub`
- Process the audio in chunks using Google Speech Recognition
- Generate a transcript from the spoken content

## Project Architecture

### Component Interaction

1. **YouTubeTranscriptManager** (Main Controller)
   - Coordinates the transcription process
   - Manages fallback between subtitle and audio methods
   - Handles error reporting

2. **YouTubeTranscriptExtractor** (Subtitle Handler)
   - Processes YouTube URLs
   - Extracts video IDs
   - Manages subtitle retrieval

3. **YouTubeAudioManager** (Audio Handler)
   - Downloads audio content
   - Manages audio processing
   - Handles speech recognition

## Quick Started

### Prerequisites

- Python 3.8 or higher
- `uv` package manager or `npm` package manager
- **FFmpeg**: Required for audio processing (used by `pydub`)

### Dependencies
- `youtube_transcript_api`: For subtitle extraction
- `pytubefix`: For downloading YouTube audio
- `SpeechRecognition`: For audio transcription
- `pydub`: For audio processing (requires FFmpeg)
- `mcp-python`: For MCP server implementation

### Installation

1. Clone this repository:
```bash
git clone [your-repo-url]
cd youtube_transcript_mcp
```

2. Install dependencies:
```bash
uv venv
uv pip install -r requirements.txt
```

3. Install FFmpeg:
   - **Windows**: Download FFmpeg from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your system's PATH.
   - **macOS**: Use Homebrew: `brew install ffmpeg`
   - **Linux**: Use your package manager, e.g., `sudo apt install ffmpeg` (Debian/Ubuntu)

### Running the Server

Run the server using:
```bash
uv run youtube_transcript_manager.py
```

### Configuration with Claude for Desktop

To use this server with Claude for Desktop, add the following to your Claude configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
    "mcpServers": {
        "youtube_transcript": {
            "command": "uv",
            "args": [
                "--directory",
                "PATH_TO_YOUR_PROJECT_FOLDER",
                "run",
                "youtube_transcript_manager.py"
            ]
        }
    }
}
```

Replace `PATH_TO_YOUR_PROJECT_FOLDER` with the absolute path to your project directory.

## MCP Server Usage

The server provides a single powerful tool `get_youtube_transcript` with the following parameters:

```python
async def get_youtube_transcript(
    url: str,                           # YouTube video URL
    languages: Optional[List[str]] = None,  # Preferred subtitle languages
    use_audio: bool = False             # Force audio-based transcription
) -> str:                               # Returns the transcript text
```

### Example Usage

1. To get transcript using available subtitles:
```python
transcript = await get_youtube_transcript("https://www.youtube.com/watch?v=VIDEO_ID")
```

2. To get transcript in specific languages:
```python
transcript = await get_youtube_transcript(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    languages=["en", "es"]
)
```

3. To force audio-based transcription:
```python
transcript = await get_youtube_transcript(
    "https://www.youtube.com/watch?v=VIDEO_ID",
    use_audio=True
)
```

