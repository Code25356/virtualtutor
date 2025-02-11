import pytest
from app.services.tts_service import TTSService
from unittest.mock import patch, MagicMock
from pathlib import Path

@pytest.fixture
def tts_service():
    with patch('google.cloud.texttospeech.TextToSpeechClient'):
        return TTSService('dummy-credentials.json', audio_dir='/tmp/test_audio')

def test_generate_audio(tts_service):
    mock_response = MagicMock()
    mock_response.audio_content = b'test audio content'
    
    with patch.object(tts_service.client, 'synthesize_speech', return_value=mock_response):
        with patch('builtins.open', create=True) as mock_open:
            filepath = tts_service.generate_audio('Test text')
            
            mock_open.assert_called_once()
            assert isinstance(filepath, str)
            assert filepath.endswith('.mp3')

def test_generate_audio_caching(tts_service):
    # Test that same text returns cached file
    mock_response = MagicMock()
    mock_response.audio_content = b'test audio content'
    
    with patch.object(tts_service.client, 'synthesize_speech', return_value=mock_response):
        with patch('pathlib.Path.exists', return_value=True):
            filepath1 = tts_service.generate_audio('Test text')
            filepath2 = tts_service.generate_audio('Test text')
            
            assert filepath1 == filepath2
            assert tts_service.client.synthesize_speech.call_count == 0

def test_generate_quiz_audio(tts_service):
    questions = [
        {
            'text': 'Test question?',
            'options': [
                {'text': 'Option 1'},
                {'text': 'Option 2'}
            ]
        }
    ]
    
    mock_response = MagicMock()
    mock_response.audio_content = b'test audio content'
    
    with patch.object(tts_service.client, 'synthesize_speech', return_value=mock_response):
        with patch('builtins.open', create=True):
            result = tts_service.generate_quiz_audio(questions)
            
            assert 'audio_url' in result[0]
            assert 'audio_url' in result[0]['options'][0]
            assert 'audio_url' in result[0]['options'][1]

def test_invalid_language(tts_service):
    with patch.object(tts_service.client, 'synthesize_speech') as mock_synthesize:
        mock_synthesize.side_effect = Exception('Invalid language')
        
        with pytest.raises(ValueError):
            tts_service.generate_audio('Test text', language='invalid')