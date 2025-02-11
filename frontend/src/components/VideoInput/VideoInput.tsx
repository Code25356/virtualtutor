import React, { useState } from 'react';
import { TextField, Button, Box, Typography } from '@mui/material';
import { useDispatch } from 'react-redux';
import { setUrl, setError } from '../../store/videoSlice';
import { api } from '../../services/api';

export const VideoInput: React.FC = () => {
  const [inputUrl, setInputUrl] = useState('');
  const dispatch = useDispatch();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const isValid = await api.validateVideoUrl(inputUrl);
      if (isValid) {
        dispatch(setUrl(inputUrl));
      } else {
        dispatch(setError('Invalid YouTube URL'));
      }
    } catch (error) {
      dispatch(setError('Error validating URL'));
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ width: '100%', maxWidth: 600, mx: 'auto' }}>
      <Typography variant="h6" gutterBottom>
        Enter YouTube Video URL
      </Typography>
      <TextField
        fullWidth
        variant="outlined"
        placeholder="https://www.youtube.com/watch?v=..."
        value={inputUrl}
        onChange={(e) => setInputUrl(e.target.value)}
        sx={{ mb: 2 }}
      />
      <Button
        type="submit"
        variant="contained"
        color="primary"
        fullWidth
      >
        Process Video
      </Button>
    </Box>
  );
};