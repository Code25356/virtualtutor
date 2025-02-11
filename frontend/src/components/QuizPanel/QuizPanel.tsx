import React from 'react';
import { Box, Typography, Button, Paper, Stack } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../../store';
import { answerQuestion, setCurrentQuestion } from '../../store/quizSlice';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';

export const QuizPanel: React.FC = () => {
  const dispatch = useDispatch();
  const { questions, currentQuestionIndex, userAnswers } = useSelector(
    (state: RootState) => state.quiz
  );
  const currentQuestion = questions[currentQuestionIndex];

  const playAudio = (audioUrl: string) => {
    const audio = new Audio(audioUrl);
    audio.play();
  };

  const handleAnswer = (answer: number) => {
    if (!currentQuestion) return;
    
    dispatch(answerQuestion({ questionId: currentQuestion.id, answer }));
    
    // Move to next question after a short delay
    setTimeout(() => {
      if (currentQuestionIndex < questions.length - 1) {
        dispatch(setCurrentQuestion(currentQuestionIndex + 1));
      }
    }, 1000);
  };

  if (!currentQuestion) return null;

  const isAnswered = userAnswers[currentQuestion.id] !== undefined;

  return (
    <Paper elevation={3} sx={{ p: 3, mt: 2, maxWidth: 600, mx: 'auto' }}>
      <Stack spacing={2}>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Typography variant="h6">
            Question {currentQuestionIndex + 1} of {questions.length}
          </Typography>
          {currentQuestion.audioUrl && (
            <Button
              startIcon={<VolumeUpIcon />}
              onClick={() => playAudio(currentQuestion.audioUrl!)}
            >
              Play Audio
            </Button>
          )}
        </Box>

        <Typography>{currentQuestion.text}</Typography>

        <Stack spacing={1}>
          {currentQuestion.options.map((option, index) => (
            <Button
              key={index}
              variant="outlined"
              onClick={() => handleAnswer(index)}
              disabled={isAnswered}
              color={
                isAnswered
                  ? index === currentQuestion.correctAnswer
                    ? 'success'
                    : userAnswers[currentQuestion.id] === index
                    ? 'error'
                    : 'primary'
                  : 'primary'
              }
              fullWidth
            >
              {option}
            </Button>
          ))}
        </Stack>
      </Stack>
    </Paper>
  );
};