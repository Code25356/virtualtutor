import React from 'react';
import { Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { Provider } from 'react-redux';
import { store } from './store';
import { theme } from './theme';

import { Home } from './pages/Home/Home';
import { Lesson } from './pages/Lesson/Lesson';
import { Summary } from './pages/Summary/Summary';

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/lesson" element={<Lesson />} />
          <Route path="/summary" element={<Summary />} />
        </Routes>
      </ThemeProvider>
    </Provider>
  );
}

export default App;
