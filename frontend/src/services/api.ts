import axios from 'axios';
import { Question } from '../store/quizSlice';

const API_BASE_URL = '/api';

interface ProcessVideoResponse {
  questions: Question[];
  videoId: string;
}

export const api = {
  async processVideo(url: string, language: string): Promise<ProcessVideoResponse> {
    const response = await axios.post(`${API_BASE_URL}/process-video`, {
      url,
      language,
    });
    return response.data;
  },

  async getAudioUrl(text: string, language: string): Promise<string> {
    const response = await axios.post(`${API_BASE_URL}/text-to-speech`, {
      text,
      language,
    });
    return response.data.audioUrl;
  },

  async validateVideoUrl(url: string): Promise<boolean> {
    try {
      const response = await axios.post(`${API_BASE_URL}/validate-video`, { url });
      return response.data.valid;
    } catch (error) {
      return false;
    }
  },
};