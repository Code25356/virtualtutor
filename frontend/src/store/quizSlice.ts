import { createSlice, PayloadAction } from '@reduxjs/toolkit';

export interface Question {
  id: string;
  text: string;
  options: string[];
  correctAnswer: number;
  audioUrl?: string;
  timestamp: number;
}

interface QuizState {
  questions: Question[];
  currentQuestionIndex: number;
  userAnswers: Record<string, number>;
  score: number;
  totalQuestions: number;
  isComplete: boolean;
}

const initialState: QuizState = {
  questions: [],
  currentQuestionIndex: 0,
  userAnswers: {},
  score: 0,
  totalQuestions: 0,
  isComplete: false,
};

const quizSlice = createSlice({
  name: 'quiz',
  initialState,
  reducers: {
    setQuestions: (state, action: PayloadAction<Question[]>) => {
      state.questions = action.payload;
      state.totalQuestions = action.payload.length;
      state.currentQuestionIndex = 0;
      state.userAnswers = {};
      state.score = 0;
      state.isComplete = false;
    },
    answerQuestion: (state, action: PayloadAction<{ questionId: string; answer: number }>) => {
      const { questionId, answer } = action.payload;
      state.userAnswers[questionId] = answer;
      
      // Update score
      const question = state.questions.find(q => q.id === questionId);
      if (question && question.correctAnswer === answer) {
        state.score += 1;
      }
    },
    setCurrentQuestion: (state, action: PayloadAction<number>) => {
      state.currentQuestionIndex = action.payload;
    },
    completeQuiz: (state) => {
      state.isComplete = true;
    },
    resetQuiz: (state) => {
      state.currentQuestionIndex = 0;
      state.userAnswers = {};
      state.score = 0;
      state.isComplete = false;
    },
  },
});

export const { setQuestions, answerQuestion, setCurrentQuestion, completeQuiz, resetQuiz } = quizSlice.actions;
export default quizSlice.reducer;