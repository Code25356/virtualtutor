import React, { useEffect } from 'react';
import { Container, Grid } from '@mui/material';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store';
import { VideoPlayer } from '../../components/VideoPlayer/VideoPlayer';
import { QuizPanel } from '../../components/QuizPanel/QuizPanel';
import { LoadingScreen } from '../../components/LoadingScreen/LoadingScreen';
import { setQuestions, setCurrentQuestion } from '../../store/quizSlice';

export const Lesson: React.FC = () => {
  const dispatch = useDispatch();
  const { isProcessing } = useSelector((state: RootState) => state.video);
  const { questions, currentQuestionIndex } = useSelector((state: RootState) => state.quiz);
  const currentTime = useSelector((state: RootState) => state.video.currentTime);

  // Monitor video time and show relevant questions
  useEffect(() => {
    if (questions.length > 0) {
      const nextQuestionIndex = questions.findIndex(
        (q, index) => index > currentQuestionIndex && q.timestamp <= currentTime
      );
      
      if (nextQuestionIndex !== -1) {
        dispatch(setCurrentQuestion(nextQuestionIndex));
      }
    }
  }, [currentTime, questions, currentQuestionIndex, dispatch]);

  if (isProcessing) {
    return <LoadingScreen />;
  }

  return (
    <Container maxWidth="lg">
      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <VideoPlayer />
        </Grid>
        <Grid item xs={12} md={4}>
          <QuizPanel />
        </Grid>
      </Grid>
    </Container>
  );
};