import React from 'react';
import { Container } from '@mui/material';
import { ScoreSummary } from '../../components/ScoreSummary/ScoreSummary';

export const Summary: React.FC = () => {
  return (
    <Container maxWidth="md">
      <ScoreSummary />
    </Container>
  );
};