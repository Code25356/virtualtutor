import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface VideoState {
  url: string;
  isProcessing: boolean;
  error: string | null;
  selectedLanguage: 'en' | 'es' | 'hi';
  currentTime: number;
}

const initialState: VideoState = {
  url: '',
  isProcessing: false,
  error: null,
  selectedLanguage: 'en',
  currentTime: 0,
};

const videoSlice = createSlice({
  name: 'video',
  initialState,
  reducers: {
    setUrl: (state, action: PayloadAction<string>) => {
      state.url = action.payload;
      state.error = null;
    },
    setProcessing: (state, action: PayloadAction<boolean>) => {
      state.isProcessing = action.payload;
    },
    setError: (state, action: PayloadAction<string | null>) => {
      state.error = action.payload;
    },
    setLanguage: (state, action: PayloadAction<'en' | 'es' | 'hi'>) => {
      state.selectedLanguage = action.payload;
    },
    setCurrentTime: (state, action: PayloadAction<number>) => {
      state.currentTime = action.payload;
    },
  },
});

export const { setUrl, setProcessing, setError, setLanguage, setCurrentTime } = videoSlice.actions;
export default videoSlice.reducer;