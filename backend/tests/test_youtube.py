import pytest
from app.services.youtube import YouTubeService
from unittest.mock import patch, MagicMock

@pytest.fixture
def youtube_service():
    return YouTubeService(temp_dir="/tmp/test_videos")

def test_get_video_info(youtube_service):
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_instance = MagicMock()
        mock_instance.extract_info.return_value = {
            'title': 'Test Video',
            'duration': 120
        }
        mock_ydl.return_value.__enter__.return_value = mock_instance
        
        info = youtube_service._get_video_info('test123')
        assert info['title'] == 'Test Video'
        assert info['duration'] == 120

def test_download_video(youtube_service):
    with patch('yt_dlp.YoutubeDL') as mock_ydl:
        mock_instance = MagicMock()
        mock_instance.extract_info.return_value = {'title': 'Test Video'}
        mock_ydl.return_value.__enter__.return_value = mock_instance
        
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.read.return_value = 'Test transcript'
            
            with patch('os.path.exists') as mock_exists:
                mock_exists.return_value = True
                
                title, transcript = youtube_service.download_video('test123')
                assert title == 'Test Video'
                assert transcript == 'Test transcript'

def test_extract_transcript_text(youtube_service):
    vtt_content = """WEBVTT

1
00:00:00.000 --> 00:00:05.000
First line of text

2
00:00:05.000 --> 00:00:10.000
Second line of text"""

    clean_text = youtube_service.extract_transcript_text(vtt_content)
    assert clean_text == 'First line of text Second line of text'

def test_invalid_video_id(youtube_service):
    with pytest.raises(ValueError):
        youtube_service.download_video('invalid_id')