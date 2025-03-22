#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting deployment process..."

# Check if env_variables.yaml exists
if [ ! -f "env_variables.yaml" ]; then
    echo "❌ env_variables.yaml not found. Please create it from the template."
    exit 1
fi

# Check if SECRET_KEY is properly set
if grep -q 'SECRET_KEY: "your-generated-secret-key"' env_variables.yaml; then
    echo "❌ Default SECRET_KEY detected in env_variables.yaml. Please generate a secure key using backend/scripts/generate_key.py"
    exit 1
fi

# Build frontend
echo "📦 Building frontend..."
cd frontend
npm install
npm run build
cd ..

# Install backend dependencies
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Verify Google Cloud SDK installation
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK not found. Please install it first."
    exit 1
fi

# Deploy to Google App Engine
echo "🚀 Deploying to Google App Engine..."
gcloud app deploy app.yaml --quiet

echo "✅ Deployment completed successfully!"
echo "🌎 Visit your application at: https://YOUR-PROJECT-ID.appspot.com"
