from datetime import datetime
from sqlalchemy import DateTime
from app import db

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'), nullable=False)
    language = db.Column(db.String(10), default='en')
    created_at = db.Column(DateTime, default=datetime.utcnow)
    questions = db.relationship('Question', backref='quiz', lazy=True)

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    audio_url = db.Column(db.String(500))
    options = db.relationship('QuestionOption', backref='question', lazy=True)
    explanation = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'audio_url': self.audio_url,
            'options': [opt.to_dict() for opt in self.options],
            'explanation': self.explanation
        }

class QuestionOption(db.Model):
    __tablename__ = 'question_options'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    audio_url = db.Column(db.String(500))
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'audio_url': self.audio_url
        }

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # We'll link this to auth system later
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option_id = db.Column(db.Integer, db.ForeignKey('question_options.id'), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'question_id': self.question_id,
            'selected_option_id': self.selected_option_id,
            'created_at': self.created_at.isoformat()
        }