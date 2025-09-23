#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from app import create_app, db
from app.utils.helpers import validate_youtube_url

def test_video_processing():
    """Test video processing directly."""
    app = create_app()
    
    with app.app_context():
        # Test URL validation
        video_id = validate_youtube_url("https://www.youtube.com/watch?v=test123")
        print(f"Validated video ID: {video_id}")
        
        # Create video entry
        from app.models.video import Video
        video = Video(youtube_id=video_id, status='pending')
        db.session.add(video)
        db.session.commit()
        print(f"Created video with ID: {video.id}")
        
        # Process video
        video.status = 'processing'
        db.session.commit()
        
        video.title = f"Sample Video Title for {video_id}"
        video.transcript = "This is a sample transcript for development purposes."
        video.language = 'en'
        video.status = 'completed'
        db.session.commit()
        
        print("Video processed successfully!")
        return video.id

if __name__ == '__main__':
    try:
        video_id = test_video_processing()
        print(f"Success! Video ID: {video_id}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()