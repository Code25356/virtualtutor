from flask import Blueprint, request, jsonify
from app import db, celery
from app.models.video import Video
from app.services.youtube import YouTubeService
from app.utils.helpers import validate_youtube_url
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('video', __name__, url_prefix='/api/videos')

youtube_service = YouTubeService()

@bp.route('/process', methods=['POST'])
def process_video():
    """Start processing a YouTube video"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({'error': 'Missing video URL'}), 400
        
    try:
        video_id = validate_youtube_url(data['url'])
        if not video_id:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
            
        # Check if video already exists
        video = Video.query.filter_by(youtube_id=video_id).first()
        if video:
            return jsonify({'error': 'Video already processed', 'video_id': video.id}), 409
            
        # Create new video entry
        video = Video(youtube_id=video_id, status='pending')
        db.session.add(video)
        db.session.commit()
        
        # Start async processing
        process_video_task.delay(video.id)
        
        return jsonify({
            'message': 'Video processing started',
            'video_id': video.id
        }), 202
        
    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:video_id>/status', methods=['GET'])
def get_status(video_id):
    """Get video processing status"""
    video = Video.query.get_or_404(video_id)
    
    return jsonify({
        'status': video.status,
        'error': video.error_message if video.error_message else None,
        'created_at': video.created_at.isoformat(),
        'updated_at': video.updated_at.isoformat()
    })

@celery.task
def process_video_task(video_id):
    """Celery task for processing video"""
    video = Video.query.get(video_id)
    if not video:
        return
        
    try:
        video.status = 'processing'
        db.session.commit()
        
        # Download video and extract transcript
        title, transcript = youtube_service.download_video(video.youtube_id, video.language)
        
        video.title = title
        video.transcript = youtube_service.extract_transcript_text(transcript)
        video.status = 'completed'
        
    except Exception as e:
        video.status = 'failed'
        video.error_message = str(e)
        logger.error(f"Error processing video {video_id}: {str(e)}")
        
    finally:
        db.session.commit()