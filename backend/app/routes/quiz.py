from flask import Blueprint, request, jsonify
from app import db
from app.models.video import Video
from app.models.quiz import Quiz, Question, QuestionOption, UserAnswer
from app.services.openai_service import OpenAIService
from app.services.tts_service import TTSService
import logging

logger = logging.getLogger(__name__)
bp = Blueprint('quiz', __name__, url_prefix='/api/videos')

openai_service = OpenAIService(api_key='your-openai-key')  # Configure in environment
tts_service = TTSService(credentials_path='path-to-credentials')  # Configure in environment

@bp.route('/<int:video_id>/quiz', methods=['GET'])
def get_quiz(video_id):
    """Get or generate quiz for video"""
    video = Video.query.get_or_404(video_id)
    
    if video.status != 'completed':
        return jsonify({'error': 'Video processing not completed'}), 400
        
    # Check if quiz already exists
    quiz = Quiz.query.filter_by(video_id=video_id).first()
    
    if not quiz:
        try:
            # Generate new quiz
            questions_data = openai_service.generate_quiz(
                video.transcript,
                language=video.language
            )
            
            # Generate audio for questions and options
            questions_data = tts_service.generate_quiz_audio(
                questions_data,
                language=video.language
            )
            
            # Create quiz in database
            quiz = Quiz(video_id=video_id, language=video.language)
            db.session.add(quiz)
            db.session.flush()
            
            for q_data in questions_data:
                question = Question(
                    quiz_id=quiz.id,
                    text=q_data['text'],
                    audio_url=q_data['audio_url'],
                    explanation=q_data['explanation']
                )
                db.session.add(question)
                db.session.flush()
                
                for opt_data in q_data['options']:
                    option = QuestionOption(
                        question_id=question.id,
                        text=opt_data['text'],
                        is_correct=opt_data['is_correct'],
                        audio_url=opt_data['audio_url']
                    )
                    db.session.add(option)
                    
            db.session.commit()
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            return jsonify({'error': str(e)}), 500
            
    # Return quiz data
    questions = Question.query.filter_by(quiz_id=quiz.id).all()
    return jsonify({
        'quiz_id': quiz.id,
        'questions': [q.to_dict() for q in questions]
    })

@bp.route('/<int:video_id>/answers', methods=['POST'])
def submit_answers(video_id):
    """Submit quiz answers"""
    data = request.get_json()
    
    if not data or 'answers' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing required data'}), 400
        
    try:
        # Validate video exists and is completed
        video = Video.query.get_or_404(video_id)
        if video.status != 'completed':
            return jsonify({'error': 'Video processing not completed'}), 400
            
        # Get quiz
        quiz = Quiz.query.filter_by(video_id=video_id).first()
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
            
        results = []
        for answer in data['answers']:
            question_id = answer.get('question_id')
            option_id = answer.get('option_id')
            
            if not question_id or not option_id:
                continue
                
            # Save user answer
            user_answer = UserAnswer(
                user_id=data['user_id'],
                question_id=question_id,
                selected_option_id=option_id
            )
            db.session.add(user_answer)
            
            # Get correct answer for response
            question = Question.query.get(question_id)
            correct_option = QuestionOption.query.filter_by(
                question_id=question_id,
                is_correct=True
            ).first()
            
            results.append({
                'question_id': question_id,
                'correct': option_id == correct_option.id,
                'explanation': question.explanation
            })
            
        db.session.commit()
        
        return jsonify({
            'message': 'Answers submitted successfully',
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Error submitting answers: {str(e)}")
        return jsonify({'error': str(e)}), 500