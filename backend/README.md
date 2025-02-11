# Video Quiz Generator Backend

This is the backend service for the Video Quiz Generator application. It processes YouTube videos, generates quizzes using OpenAI, and provides text-to-speech functionality.

## Features

- YouTube video processing and transcript extraction
- Quiz generation using OpenAI GPT-4
- Text-to-speech using Google Cloud TTS
- RESTful API endpoints
- Celery task queue for async processing
- SQLAlchemy ORM with database migrations
- Comprehensive test suite

## Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
export FLASK_APP=run.py
export FLASK_ENV=development
export OPENAI_API_KEY=your-openai-key
export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
```

4. Initialize the database:
```bash
flask db upgrade
```

5. Start Redis (required for Celery):
```bash
redis-server
```

6. Start Celery worker:
```bash
celery -A app.celery worker --loglevel=info
```

7. Run the application:
```bash
flask run
```

## API Endpoints

### Video Processing

- `POST /api/videos/process`
  - Process a YouTube video
  - Body: `{"url": "youtube-url"}`

- `GET /api/videos/{video_id}/status`
  - Get video processing status

### Quiz

- `GET /api/videos/{video_id}/quiz`
  - Get generated quiz for video

- `POST /api/videos/{video_id}/answers`
  - Submit quiz answers
  - Body: `{"user_id": 123, "answers": [{"question_id": 1, "option_id": 2}, ...]}`

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # Database models
│   ├── services/        # Business logic services
│   ├── routes/          # API endpoints
│   └── utils/           # Helper functions
├── tests/               # Test suite
├── config.py           # Configuration
└── run.py             # Application entry point
```

## Dependencies

- Flask - Web framework
- SQLAlchemy - ORM
- Celery - Task queue
- yt-dlp - YouTube video processing
- OpenAI - Quiz generation
- Google Cloud TTS - Text-to-speech
- Redis - Cache and message broker
- pytest - Testing framework