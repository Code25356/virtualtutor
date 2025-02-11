import logging
from typing import List, Dict
import openai
from app.utils.helpers import chunk_text

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        
    def generate_quiz(self, transcript: str, language: str = 'en', num_questions: int = 5) -> List[Dict]:
        """
        Generate quiz questions from video transcript using OpenAI
        Returns list of questions with options and correct answers
        """
        # Split transcript into chunks if too long
        chunks = chunk_text(transcript, max_tokens=3000)
        
        system_prompt = {
            'en': """You are a quiz generator. Generate multiple choice questions based on the given text. 
                    Each question should have 4 options with one correct answer. Include an explanation for the correct answer.""",
            'es': """Eres un generador de cuestionarios. Genera preguntas de opción múltiple basadas en el texto dado.
                    Cada pregunta debe tener 4 opciones con una respuesta correcta. Incluye una explicación para la respuesta correcta."""
            # Add more languages as needed
        }
        
        questions = []
        
        try:
            for chunk in chunks:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": system_prompt.get(language, system_prompt['en'])},
                        {"role": "user", "content": f"Generate {num_questions} multiple choice questions from this text: {chunk}"}
                    ],
                    temperature=0.7,
                    max_tokens=2000
                )
                
                # Parse the response and format questions
                raw_questions = self._parse_questions(response.choices[0].message.content)
                questions.extend(raw_questions)
                
            return questions[:num_questions]  # Ensure we only return requested number of questions
            
        except Exception as e:
            logger.error(f"Error generating quiz: {str(e)}")
            raise ValueError(f"Failed to generate quiz: {str(e)}")
            
    def _parse_questions(self, raw_text: str) -> List[Dict]:
        """Parse OpenAI response into structured question format"""
        questions = []
        current_question = None
        
        for line in raw_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            if line.startswith(('Q:', 'Question:')):
                if current_question:
                    questions.append(current_question)
                current_question = {
                    'text': line.split(':', 1)[1].strip(),
                    'options': [],
                    'correct_answer': None,
                    'explanation': None
                }
            elif line.startswith(('A:', 'B:', 'C:', 'D:')):
                option = {
                    'text': line[2:].strip(),
                    'is_correct': False
                }
                current_question['options'].append(option)
            elif line.startswith(('Correct Answer:', 'Answer:')):
                correct = line.split(':')[1].strip()
                if correct in ['A', 'B', 'C', 'D']:
                    idx = ord(correct) - ord('A')
                    if idx < len(current_question['options']):
                        current_question['options'][idx]['is_correct'] = True
            elif line.startswith(('Explanation:', 'E:')):
                current_question['explanation'] = line.split(':', 1)[1].strip()
                
        if current_question:
            questions.append(current_question)
            
        return questions