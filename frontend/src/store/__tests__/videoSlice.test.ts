import videoReducer, {
  setUrl,
  setProcessing,
  setError,
  setLanguage,
} from '../videoSlice';

describe('videoSlice', () => {
  const initialState = {
    url: '',
    isProcessing: false,
    error: null,
    selectedLanguage: 'en',
    currentTime: 0,
  };

  it('should handle initial state', () => {
    expect(videoReducer(undefined, { type: 'unknown' })).toEqual(initialState);
  });

  it('should handle setUrl', () => {
    const url = 'https://youtube.com/watch?v=test';
    const actual = videoReducer(initialState, setUrl(url));
    expect(actual.url).toEqual(url);
    expect(actual.error).toBeNull();
  });

  it('should handle setProcessing', () => {
    const actual = videoReducer(initialState, setProcessing(true));
    expect(actual.isProcessing).toEqual(true);
  });

  it('should handle setError', () => {
    const error = 'Test error';
    const actual = videoReducer(initialState, setError(error));
    expect(actual.error).toEqual(error);
  });

  it('should handle setLanguage', () => {
    const actual = videoReducer(initialState, setLanguage('es'));
    expect(actual.selectedLanguage).toEqual('es');
  });
});