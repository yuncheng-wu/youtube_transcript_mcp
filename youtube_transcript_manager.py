from typing import Optional, List
from youtube_audio import YouTubeAudioManager
from youtube_transcript import YouTubeTranscriptExtractor
from mcp.server.fastmcp import FastMCP
import uvicorn

class YouTubeTranscriptManager:
    """
    A class to manage YouTube video transcription using either subtitles or audio-based transcription.
    Integrates both subtitle-based and audio-based transcription methods.
    """
    
    @staticmethod
    def get_transcript(url: str, languages: Optional[List[str]] = None, use_audio: bool = False) -> str:
        """
        Get transcript from a YouTube video using either subtitles or audio transcription.
        
        Args:
            url: The YouTube video URL
            languages: Optional list of language codes for subtitle preference
            use_audio: Force using audio-based transcription even if subtitles are available
            
        Returns:
            str: The transcript text
            
        Raises:
            ValueError: If the YouTube URL is invalid
            Exception: If transcription fails
        """
        # Get video ID from URL
        video_id = YouTubeTranscriptExtractor.get_youtube_video_id(url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")

        # First try to get transcript from subtitles
        if not use_audio:
            print("Trying subtitle-based transcription...")
            transcript = YouTubeTranscriptExtractor.get_transcript(video_id, languages)
            if transcript:
                print("Subtitles found, using subtitle-based transcription...")
                return transcript
            print("No subtitles available, falling back to audio-based transcription...")

        # If subtitles are not available or failed, use audio-based transcription
        print("Using audio-based transcription...")
        try:
            # Clear any existing temporary files
            YouTubeAudioManager.clear_temp()
            
            # Get and transcribe the audio
            audio = YouTubeAudioManager.get_youtube_audio(url)
            transcript = YouTubeAudioManager.transcribe_audio(audio)
            
            # Clean up temporary files
            YouTubeAudioManager.clear_temp()
            
            return transcript
        except Exception as e:
            raise Exception(f"Failed to get transcript: {str(e)}")

mcp = FastMCP()

@mcp.tool()
async def get_youtube_transcript(url: str, languages: Optional[List[str]] = None, use_audio: bool = False) -> str:
    """Get transcript from a YouTube video using either subtitles or audio transcription.
    
    Args:
        url: The YouTube video URL
        languages: Optional list of language codes for subtitle preference
        use_audio: Force using audio-based transcription even if subtitles are available
        
    Returns:
        str: The transcript text
    """
    try:
        return YouTubeTranscriptManager.get_transcript(url, languages, use_audio)
    except Exception as e:
        raise Exception(f"Failed to get transcript: {str(e)}")

def main():
    """Start the MCP server"""
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    main()
