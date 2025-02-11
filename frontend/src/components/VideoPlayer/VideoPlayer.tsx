import React, { useEffect, useRef } from 'react';
import { Box } from '@mui/material';
import { useDispatch, useSelector } from 'react-redux';
import { setCurrentTime } from '../../store/videoSlice';
import { RootState } from '../../store';
import YouTube from 'react-youtube';

export const VideoPlayer: React.FC = () => {
  const dispatch = useDispatch();
  const url = useSelector((state: RootState) => state.video.url);
  const playerRef = useRef<any>(null);

  const getVideoId = (url: string) => {
    const match = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&?]+)/);
    return match ? match[1] : '';
  };

  const onStateChange = (event: any) => {
    // Update current time every second when playing
    if (event.data === YouTube.PlayerState.PLAYING) {
      const interval = setInterval(() => {
        const currentTime = playerRef.current?.getCurrentTime() || 0;
        dispatch(setCurrentTime(currentTime));
      }, 1000);

      return () => clearInterval(interval);
    }
  };

  const opts = {
    height: '390',
    width: '640',
    playerVars: {
      autoplay: 0,
    },
  };

  return (
    <Box sx={{ width: '100%', maxWidth: 640, mx: 'auto', mt: 2 }}>
      <YouTube
        videoId={getVideoId(url)}
        opts={opts}
        onStateChange={onStateChange}
        ref={playerRef}
      />
    </Box>
  );
};