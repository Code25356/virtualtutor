import React from 'react';
import { Box, Typography, Paper, Button, Stack } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { resetQuiz } from '../../store/quizSlice';
import { setUrl } from '../../store/videoSlice';

export const ScoreSummary: React.FC = () => {
  const dispatch = useDispatch();
  const { score, totalQuestions, userAnswers, questions } = useSelector(
    (state: RootState) => state.quiz
  );

  const percentage = Math.round((score / totalQuestions) * 100);

  const handleTryAgain = () => {
    dispatch(resetQuiz());
    dispatch(setUrl(''));
  };

  return (
    <Paper elevation={3} sx={{ p: 4, maxWidth: 600, mx: 'auto', mt: 4 }}>
      <Stack spacing={3}>
        <Typography variant="h4" align="center">
          Quiz Complete!
        </Typography>

        <Box textAlign="center">
          <Typography variant="h2" color="primary">
            {percentage}%
          </Typography>
          <Typography variant="h6">
            {score} out of {totalQuestions} correct
          </Typography>
        </Box>

        <Box>
          <Typography variant="h6" gutterBottom>
            Question Summary:
          </Typography>
          {questions.map((question, index) => (
            <Box key={question.id} sx={{ mb: 2 }}>
              <Typography variant="body1" gutterBottom>
                {index + 1}. {question.text}
              </Typography>
              <Typography
                variant="body2"
                color={
                  userAnswers[question.id] === question.correctAnswer
                    ? 'success.main'
                    : 'error.main'
                }
              >
                Your answer: {question.options[userAnswers[question.id]]}
                {userAnswers[question.id] !== question.correctAnswer && (
                  <> (Correct: {question.options[question.correctAnswer]})</>
                )}
              </Typography>
            </Box>
          ))}
        </Box>

        <Button
          variant="contained"
          color="primary"
          size="large"
          onClick={handleTryAgain}
        >
          Try Another Video
        </Button>
      </Stack>
    </Paper>
  );
};