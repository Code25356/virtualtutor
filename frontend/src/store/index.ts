import { configureStore } from '@reduxjs/toolkit';
import videoReducer from './videoSlice';
import quizReducer from './quizSlice';

export const store = configureStore({
  reducer: {
    video: videoReducer,
    quiz: quizReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;