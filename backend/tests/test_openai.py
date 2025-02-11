import pytest
from app.services.openai_service import OpenAIService
from unittest.mock import patch, MagicMock

@pytest.fixture
def openai_service():
    return OpenAIService('test-key')

def test_generate_quiz(openai_service):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="""
Q: Test question?
A: First option
B: Second option
C: Third option
D: Fourth option
Correct Answer: B
Explanation: This is the explanation
        """))
    ]
    
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        questions = openai_service.generate_quiz("Test transcript")
        
        assert len(questions) == 1
        assert questions[0]['text'] == 'Test question?'
        assert len(questions[0]['options']) == 4
        assert questions[0]['options'][1]['is_correct'] == True
        assert questions[0]['explanation'] == 'This is the explanation'

def test_parse_questions(openai_service):
    raw_text = """
Q: First question?
A: Option 1
B: Option 2
C: Option 3
D: Option 4
Correct Answer: A
Explanation: Test explanation

Q: Second question?
A: Option 1
B: Option 2
C: Option 3
D: Option 4
Correct Answer: C
Explanation: Another explanation
    """
    
    questions = openai_service._parse_questions(raw_text)
    assert len(questions) == 2
    assert questions[0]['text'] == 'First question?'
    assert questions[0]['options'][0]['is_correct'] == True
    assert questions[1]['text'] == 'Second question?'
    assert questions[1]['options'][2]['is_correct'] == True

def test_generate_quiz_with_language(openai_service):
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="""
Q: ¿Pregunta de prueba?
A: Primera opción
B: Segunda opción
C: Tercera opción
D: Cuarta opción
Correct Answer: B
Explanation: Esta es la explicación
        """))
    ]
    
    with patch('openai.ChatCompletion.create', return_value=mock_response):
        questions = openai_service.generate_quiz("Test transcript", language='es')
        
        assert len(questions) == 1
        assert questions[0]['text'] == '¿Pregunta de prueba?'
        assert questions[0]['explanation'] == 'Esta es la explicación'