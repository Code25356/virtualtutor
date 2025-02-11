import React from 'react';
import { FormControl, InputLabel, Select, MenuItem } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { setLanguage } from '../../store/videoSlice';
import { RootState } from '../../store';

const languages = [
  { code: 'en', label: 'English' },
  { code: 'es', label: 'Spanish' },
  { code: 'hi', label: 'Hindi' },
];

export const LanguageSelector: React.FC = () => {
  const dispatch = useDispatch();
  const selectedLanguage = useSelector((state: RootState) => state.video.selectedLanguage);

  return (
    <FormControl fullWidth sx={{ maxWidth: 200 }}>
      <InputLabel>Language</InputLabel>
      <Select
        value={selectedLanguage}
        label="Language"
        onChange={(e) => dispatch(setLanguage(e.target.value as 'en' | 'es' | 'hi'))}
      >
        {languages.map((lang) => (
          <MenuItem key={lang.code} value={lang.code}>
            {lang.label}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};