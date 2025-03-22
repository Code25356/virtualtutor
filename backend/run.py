import os
from app import create_app

# Use development config when running locally
app = create_app('development')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
