from youtube_transcript_manager import YouTubeTranscriptManager
from typing import Optional, List
from mcp.server.fastmcp import FastMCP

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
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()