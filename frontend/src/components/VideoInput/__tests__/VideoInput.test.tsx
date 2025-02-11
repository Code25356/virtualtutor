import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import { Provider } from 'react-redux';
import { configureStore } from '@reduxjs/toolkit';
import { VideoInput } from '../VideoInput';
import videoReducer from '../../../store/videoSlice';

const mockStore = configureStore({
  reducer: {
    video: videoReducer,
  },
});

describe('VideoInput', () => {
  it('renders input field and submit button', () => {
    render(
      <Provider store={mockStore}>
        <VideoInput />
      </Provider>
    );

    expect(screen.getByPlaceholderText(/youtube.com/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /process video/i })).toBeInTheDocument();
  });

  it('updates input value on change', () => {
    render(
      <Provider store={mockStore}>
        <VideoInput />
      </Provider>
    );

    const input = screen.getByPlaceholderText(/youtube.com/i);
    fireEvent.change(input, { target: { value: 'https://youtube.com/watch?v=test' } });
    expect(input).toHaveValue('https://youtube.com/watch?v=test');
  });
});