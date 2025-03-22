import os
import secrets
import warnings
from datetime import timedelta

class Config:
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set. Please set the SECRET_KEY environment variable.")
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # File uploads
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp/uploads')
    AUDIO_FOLDER = os.environ.get('AUDIO_FOLDER', 'static/audio')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # API Keys
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    
    # Cache
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/1')
    CACHE_DEFAULT_TIMEOUT = 300
    
    # Task timeouts
    VIDEO_PROCESSING_TIMEOUT = int(os.environ.get('VIDEO_PROCESSING_TIMEOUT', 3600))  # 1 hour
    QUIZ_GENERATION_TIMEOUT = int(os.environ.get('QUIZ_GENERATION_TIMEOUT', 300))  # 5 minutes

class DevelopmentConfig(Config):
    DEBUG = True
    
    # Override the SECRET_KEY validation for development
    @property
    def SECRET_KEY(self):
        key = os.environ.get('SECRET_KEY')
        if not key:
            # Generate a random key for development
            key = secrets.token_hex(32)
            warnings.warn(
                "Using a randomly generated SECRET_KEY. This is acceptable for local development only. "
                "Set a SECRET_KEY environment variable for consistent sessions."
            )
        return key

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CELERY_BROKER_URL = 'memory://'
    CELERY_RESULT_BACKEND = 'cache'
    WTF_CSRF_ENABLED = False
    
    # Override the SECRET_KEY validation for testing
    @property
    def SECRET_KEY(self):
        return 'test-key'
