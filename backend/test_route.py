#!/usr/bin/env python3
import sys
import os
import json
from dotenv import load_dotenv

# Add the backend directory to the path
sys.path.append(os.path.dirname(__file__))

# Load environment variables
load_dotenv()

from app import create_app

def test_video_route():
    """Test the video processing route."""
    app = create_app()
    
    with app.test_client() as client:
        # Test the video processing endpoint
        response = client.post('/api/videos/process',
                             data=json.dumps({"url": "https://www.youtube.com/watch?v=test999", "language": "en"}),
                             content_type='application/json')
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.get_json()}")
        
        return response

if __name__ == '__main__':
    try:
        response = test_video_route()
        print("Route test completed!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()