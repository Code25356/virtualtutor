# VirtualTutor

An interactive learning platform that enhances video content with AI-powered quizzes and multilingual support. The application processes YouTube videos, generates contextual quizzes, and provides real-time voice interaction for an engaging learning experience.

## Features

- YouTube video processing with multilingual support
- Real-time quiz generation using AI
- Interactive voice-based questions and answers
- Support for English, Spanish, and Hindi
- Performance analysis and scoring
- Google Cloud integration for scalability

## Project Structure

```
virtualtutor/
├── frontend/          # React frontend with TypeScript
├── backend/           # Flask backend
├── .gitignore        # Git ignore file
├── README.md         # Documentation
└── app.yaml          # Google App Engine config
```

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Git

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at http://localhost:3000

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start development server:
   ```bash
   python run.py
   ```
   The backend API will be available at http://localhost:5000

## Development Guidelines

### Frontend
- Use TypeScript for all new code
- Follow Material-UI design patterns
- Implement state management using Redux Toolkit
- Use React Router for navigation
- Keep components small and focused
- Write meaningful component and variable names

### Backend
- Follow PEP 8 style guide
- Use Flask blueprints for API organization
- Keep routes clean and focused
- Implement proper error handling
- Use environment variables for configuration
- Write clear docstrings

## Deployment Instructions

### Prerequisites

1. Install Google Cloud SDK
2. Create a Google Cloud Project
3. Enable required APIs:
   - Google App Engine Admin API
   - Cloud Storage API
   - Cloud Text-to-Speech API
   - YouTube Data API v3

### API Credentials Setup

1. Create a service account:
   ```bash
   gcloud iam service-accounts create virtualtutor-sa
   ```

2. Download service account key:
   ```bash
   gcloud iam service-accounts keys create service-account.json --iam-account=virtualtutor-sa@YOUR-PROJECT.iam.gserviceaccount.com
   ```

3. Create storage bucket:
   ```bash
   gsutil mb gs://YOUR-PROJECT-virtualtutor
   ```

### Environment Setup

1. Copy env_variables.yaml.template to env_variables.yaml:
   ```bash
   cp env_variables.yaml.template env_variables.yaml
   ```

2. Update env_variables.yaml with your credentials:
   - OpenAI API key
   - YouTube API key
   - Google Cloud project details
   - Storage bucket name
   - Secret key

### Deployment

1. Make deploy.sh executable:
   ```bash
   chmod +x deploy.sh
   ```

2. Run deployment script:
   ```bash
   ./deploy.sh
   ```

The script will:
- Build the frontend
- Install backend dependencies
- Deploy to Google App Engine

### Troubleshooting

1. **Deployment Fails**
   - Check if all required APIs are enabled
   - Verify service account permissions
   - Ensure env_variables.yaml is properly configured

2. **Video Processing Issues**
   - Check storage bucket permissions
   - Verify YouTube API quota
   - Check service account permissions

3. **Quiz Generation Issues**
   - Verify OpenAI API key
   - Check API rate limits
   - Ensure proper error handling

### Environment Variables

Create `.env` files in both frontend and backend directories:

Frontend (.env):
```
VITE_API_URL=http://localhost:5000/api
```

Backend (.env):
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

## License

This project is private and confidential.
