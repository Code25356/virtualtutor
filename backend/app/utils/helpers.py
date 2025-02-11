import re
from typing import List
import logging

logger = logging.getLogger(__name__)

def validate_youtube_url(url: str) -> str:
    """
    Extract and validate YouTube video ID from URL
    Returns video ID if valid, None otherwise
    """
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu.be\/)([\w-]+)',
        r'(?:youtube\.com\/embed\/)([\w-]+)',
        r'(?:youtube\.com\/v\/)([\w-]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def chunk_text(text: str, max_tokens: int = 3000) -> List[str]:
    """Split text into chunks of approximately max_tokens"""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    # Rough estimate: average word is 5 characters
    words_per_chunk = max_tokens // 5
    
    for word in words:
        current_chunk.append(word)
        current_length += 1
        
        if current_length >= words_per_chunk:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            current_length = 0
            
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks

def clean_filename(filename: str) -> str:
    """Clean filename to be safe for filesystem"""
    return re.sub(r'[^\w\-_.]', '_', filename)