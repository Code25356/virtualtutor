from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import logging
from logging.config import dictConfig
from pythonjsonlogger import jsonlogger
import os

# Initialize extensions
db = SQLAlchemy()
celery = Celery()

def create_app(config_name='default'):
    app = Flask(__name__)
    
    # Load config
    if config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.Config')
        
    # Configure logging
    dictConfig({
        'version': 1,
        'formatters': {
            'json': {
                '()': jsonlogger.JsonFormatter,
                'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'json',
                'filename': 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    })
    
    # Initialize extensions
    db.init_app(app)
    
    # Configure Celery
    celery.conf.update(
        broker_url=app.config['CELERY_BROKER_URL'],
        result_backend=app.config['CELERY_RESULT_BACKEND'],
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC'
    )
    
    # Register blueprints
    from app.routes import video, quiz
    app.register_blueprint(video.bp)
    app.register_blueprint(quiz.bp)
    
    # Create upload directories if they don't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)
    
    return app