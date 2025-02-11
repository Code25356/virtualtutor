import os
from google.cloud import texttospeech
import logging
from pathlib import Path
import hashlib

logger = logging.getLogger(__name__)

class TTSService:
    def __init__(self, credentials_path: str, audio_dir: str = "static/audio"):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = texttospeech.TextToSpeechClient()
        self.audio_dir = Path(audio_dir)
        self.audio_dir.mkdir(parents=True, exist_ok=True)
        
        self.language_voices = {
            'en': 'en-US-Neural2-A',
            'es': 'es-US-Neural2-A',
            # Add more languages as needed
        }
        
    def generate_audio(self, text: str, language: str = 'en') -> str:
        """
        Generate audio for text using Google Cloud TTS
        Returns the URL path to the generated audio file
        """
        # Generate unique filename based on text content
        text_hash = hashlib.md5(text.encode()).hexdigest()
        filename = f"{language}_{text_hash}.mp3"
        filepath = self.audio_dir / filename
        
        # Return existing file if already generated
        if filepath.exists():
            return str(filepath)
            
        try:
            # Configure the voice
            voice = texttospeech.VoiceSelectionParams(
                language_code=language,
                name=self.language_voices.get(language, self.language_voices['en'])
            )
            
            # Configure audio encoding
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=1.0
            )
            
            # Perform the text-to-speech request
            synthesis_input = texttospeech.SynthesisInput(text=text)
            response = self.client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Write the response to the output file
            with open(filepath, 'wb') as out:
                out.write(response.audio_content)
                
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error generating audio: {str(e)}")
            raise ValueError(f"Failed to generate audio: {str(e)}")
            
    def generate_quiz_audio(self, questions: list, language: str = 'en') -> list:
        """Generate audio for all questions and options in a quiz"""
        for question in questions:
            # Generate audio for question text
            question['audio_url'] = self.generate_audio(question['text'], language)
            
            # Generate audio for each option
            for option in question['options']:
                option['audio_url'] = self.generate_audio(option['text'], language)
                
        return questions