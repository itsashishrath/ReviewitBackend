import os
import random
import time
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

# # Get the proxy from the environment variable
# PROXY = os.getenv("PROXY", "")  # Replace with your actual proxy

# def get_captions(video_id, language_code='en', max_retries=3):
#     retry_count = 0
    
#     while retry_count < max_retries:
#         # Select the proxy for this attempt
#         proxies = {
#             "https": PROXY
#         }

#         print(f"Using proxy: {PROXY}")

#         try:
#             # Try fetching the transcript
#             transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code], proxies=proxies)
            
#             # Format the transcript
#             formatter = TextFormatter()
#             formatted_transcript = formatter.format_transcript(transcript)
            
#             return formatted_transcript
        
#         except Exception as e:
#             retry_count += 1
#             print(f"Error: {str(e)}. Retrying... ({retry_count}/{max_retries})")
            
#             if retry_count >= max_retries:
#                 return f"Failed after {max_retries} attempts. Error: {str(e)}"
            
#             # Exponential backoff with jitter
#             wait_time = (2 ** retry_count) + random.uniform(0, 1)
#             time.sleep(wait_time)
    
#     return "Could not retrieve captions after multiple attempts."

# def main():
#     # Example YouTube video ID (Replace this with the actual video ID you want to fetch)
#     video_id = "dQw4w9WgXcQ"  # Example video ID, replace with a valid one.
    
#     transcript = get_captions(video_id)
    
#     if transcript:
#         print("\nTranscript:\n")
#         print(transcript)
#     else:
#         print("No transcript available.")

# if __name__ == "__main__":
#     main()


import requests
url = 'https://ip.smartproxy.com/json'
username = 'spig2gj39p'
password = 'o3woU~3jH8TqthwqT9'
proxy = f"http://{username}:{password}@gate.smartproxy.com:10001"
result = requests.get(url, proxies = {
    'http': proxy,
    'https': proxy
})
transcript = YouTubeTranscriptApi.get_transcript('dQw4w9WgXcQ', languages=['en'], proxies = {
    'http': proxy,
    'https': proxy
})
print(result.text)
print(transcript)
