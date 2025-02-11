import pytest
from app import create_app, db
from app.models.video import Video
from app.models.quiz import Quiz, Question, QuestionOption

@pytest.fixture
def app():
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def video(app):
    with app.app_context():
        video = Video(
            youtube_id='test123',
            title='Test Video',
            status='completed',
            transcript='Test transcript content'
        )
        db.session.add(video)
        db.session.commit()
        return video

@pytest.fixture
def quiz(app, video):
    with app.app_context():
        quiz = Quiz(video_id=video.id)
        db.session.add(quiz)
        db.session.flush()
        
        question = Question(
            quiz_id=quiz.id,
            text='Test question?',
            explanation='Test explanation'
        )
        db.session.add(question)
        db.session.flush()
        
        options = [
            QuestionOption(question_id=question.id, text='Option 1', is_correct=True),
            QuestionOption(question_id=question.id, text='Option 2', is_correct=False),
            QuestionOption(question_id=question.id, text='Option 3', is_correct=False),
            QuestionOption(question_id=question.id, text='Option 4', is_correct=False)
        ]
        for option in options:
            db.session.add(option)
            
        db.session.commit()
        return quiz