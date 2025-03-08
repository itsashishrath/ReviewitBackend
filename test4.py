import requests

# Full browser-like headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Test fetching video page
response = requests.get('https://www.youtube.com/watch?v=dQw4w9WgXcQ', headers=headers)

# Check if captions JSON is in the response
if '"captions":' in response.text:
    print("Captions JSON found!")
    # Very rough extraction just for testing
    captions_part = response.text.split('"captions":')[1].split(',"videoDetails')[0]
    print(captions_part)  # Print first 200 chars
else:
    print("No captions JSON found")