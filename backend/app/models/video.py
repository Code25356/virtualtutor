from datetime import datetime
from sqlalchemy import DateTime
from app import db

class Video(db.Model):
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    youtube_id = db.Column(db.String(20), unique=True, nullable=False)
    title = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    language = db.Column(db.String(10), default='en')
    transcript = db.Column(db.Text)
    error_message = db.Column(db.Text)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'youtube_id': self.youtube_id,
            'title': self.title,
            'status': self.status,
            'language': self.language,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }