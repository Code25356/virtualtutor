import React from 'react';
import { Container, Typography, Box } from '@mui/material';
import { VideoInput } from '../../components/VideoInput/VideoInput';
import { LanguageSelector } from '../../components/LanguageSelector/LanguageSelector';

export const Home: React.FC = () => {
  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4, textAlign: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Virtual Tutor
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          Learn from any YouTube video with interactive quizzes
        </Typography>
        
        <Box sx={{ my: 4 }}>
          <LanguageSelector />
        </Box>
        
        <VideoInput />
      </Box>
    </Container>
  );
};