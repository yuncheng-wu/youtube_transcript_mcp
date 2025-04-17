from typing import Optional, List
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

class YouTubeTranscriptExtractor:
    """Handles YouTube video transcript extraction from subtitles."""
    
    @staticmethod
    def get_youtube_video_id(url: str) -> Optional[str]:
        """
        Extract video ID from a YouTube URL.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname

        if hostname == "youtu.be":
            return parsed_url.path[1:]
        if hostname in ("www.youtube.com", "youtube.com"):
            if parsed_url.path == "/watch":
                query_params = parse_qs(parsed_url.query)
                return query_params.get("v", [None])[0]
            if parsed_url.path.startswith("/embed/"):
                return parsed_url.path.split("/")[2]
            if parsed_url.path.startswith("/v/"):
                return parsed_url.path.split("/")[2]
        return None

    @staticmethod
    def get_transcript(video_id: str, languages: Optional[List[str]] = None) -> Optional[str]:
        """
        Get transcript from YouTube video subtitles.
        
        Args:
            video_id: YouTube video ID
            languages: Optional list of language codes for subtitle preference
            
        Returns:
            Optional[str]: Transcript text if found, None if no subtitles available
        """
        try:
            if languages:
                captions = YouTubeTranscriptApi.get_transcript(video_id, languages=languages)
            else:
                captions = YouTubeTranscriptApi.get_transcript(video_id)
            return " ".join(line["text"] for line in captions)
        except (NoTranscriptFound, TranscriptsDisabled) as e:
            print(f"No subtitles available: {str(e)}")
            return None
        except Exception as e:
            print(f"Error getting subtitles: {str(e)}")
            return None
