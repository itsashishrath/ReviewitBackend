import requests
from youtube_transcript_api import YouTubeTranscriptApi
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the proxy list from the environment variable
# proxies = os.getenv("PROXIES")

# Free proxy (Replace with a working one)
proxies = {
    "http":"http://tfuysuxk:9mp578cf68wd@38.154.227.167:5868"
}

# Test if the proxy works
try:
    response = requests.get("https://www.google.com", proxies=proxies, timeout=5)
    if response.status_code == 200:
        print("Proxy is working!")
except Exception as e:
    print("Proxy failed:", e)

# Function to fetch transcript using proxy
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id,languages=['en'], proxies=proxies)
        return transcript
    except Exception as e:
        return f"Error: {e}"

# Example usage
video_id = "rQqrwb9rH30"  # Replace with actual video ID
transcript = get_transcript(video_id)
print(transcript)
