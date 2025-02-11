import os
import yt_dlp
import logging
from typing import Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class YouTubeService:
    def __init__(self, temp_dir: str = "/tmp/videos"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
    def _get_video_info(self, video_id: str) -> dict:
        """Get video information using yt-dlp"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                return ydl.extract_info(f"https://www.youtube.com/watch?v={video_id}", download=False)
            except Exception as e:
                logger.error(f"Error getting video info: {str(e)}")
                raise ValueError(f"Failed to get video info: {str(e)}")

    def download_video(self, video_id: str, language: str = 'en') -> Tuple[str, str]:
        """
        Download video and extract transcript
        Returns: (title, transcript)
        """
        output_path = self.temp_dir / video_id
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': [language],
            'outtmpl': str(output_path),
            'quiet': True,
            'no_warnings': True
        }
        
        try:
            # Get video info first
            info = self._get_video_info(video_id)
            title = info.get('title', '')
            
            # Download video and subtitles
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([f"https://www.youtube.com/watch?v={video_id}"])
            
            # Read transcript
            transcript_path = output_path + f".{language}.vtt"
            if os.path.exists(transcript_path):
                with open(transcript_path, 'r', encoding='utf-8') as f:
                    transcript = f.read()
            else:
                raise FileNotFoundError(f"No transcript found for language: {language}")
            
            return title, transcript
            
        except Exception as e:
            logger.error(f"Error downloading video: {str(e)}")
            raise ValueError(f"Failed to download video: {str(e)}")
        
        finally:
            # Cleanup temporary files
            for file in output_path.parent.glob(f"{video_id}*"):
                try:
                    file.unlink()
                except Exception as e:
                    logger.warning(f"Failed to delete temporary file {file}: {str(e)}")
                    
    def extract_transcript_text(self, transcript: str) -> str:
        """Extract clean text from VTT transcript"""
        lines = transcript.split('\n')
        text_lines = []
        
        for line in lines:
            # Skip timestamp lines and empty lines
            if '-->' in line or not line.strip() or line.strip().isdigit():
                continue
            text_lines.append(line.strip())
            
        return ' '.join(text_lines)