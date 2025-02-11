import quizReducer, {
  setQuestions,
  answerQuestion,
  setCurrentQuestion,
  completeQuiz,
  resetQuiz,
  Question,
} from '../quizSlice';

describe('quizSlice', () => {
  const initialState = {
    questions: [],
    currentQuestionIndex: 0,
    userAnswers: {},
    score: 0,
    totalQuestions: 0,
    isComplete: false,
  };

  const sampleQuestions: Question[] = [
    {
      id: '1',
      text: 'Test question 1',
      options: ['A', 'B', 'C', 'D'],
      correctAnswer: 2,
      timestamp: 10,
    },
    {
      id: '2',
      text: 'Test question 2',
      options: ['A', 'B', 'C', 'D'],
      correctAnswer: 1,
      timestamp: 20,
    },
  ];

  it('should handle initial state', () => {
    expect(quizReducer(undefined, { type: 'unknown' })).toEqual(initialState);
  });

  it('should handle setQuestions', () => {
    const actual = quizReducer(initialState, setQuestions(sampleQuestions));
    expect(actual.questions).toEqual(sampleQuestions);
    expect(actual.totalQuestions).toEqual(2);
  });

  it('should handle answerQuestion with correct answer', () => {
    const state = {
      ...initialState,
      questions: sampleQuestions,
      totalQuestions: 2,
    };
    const actual = quizReducer(
      state,
      answerQuestion({ questionId: '1', answer: 2 })
    );
    expect(actual.userAnswers['1']).toEqual(2);
    expect(actual.score).toEqual(1);
  });

  it('should handle setCurrentQuestion', () => {
    const actual = quizReducer(initialState, setCurrentQuestion(1));
    expect(actual.currentQuestionIndex).toEqual(1);
  });

  it('should handle completeQuiz', () => {
    const actual = quizReducer(initialState, completeQuiz());
    expect(actual.isComplete).toEqual(true);
  });

  it('should handle resetQuiz', () => {
    const state = {
      ...initialState,
      currentQuestionIndex: 5,
      userAnswers: { '1': 2 },
      score: 10,
      isComplete: true,
    };
    const actual = quizReducer(state, resetQuiz());
    expect(actual.currentQuestionIndex).toEqual(0);
    expect(actual.userAnswers).toEqual({});
    expect(actual.score).toEqual(0);
    expect(actual.isComplete).toEqual(false);
  });
});