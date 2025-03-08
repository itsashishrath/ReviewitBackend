import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_youtube_transcript(video_id):
    """
    Extract transcript from YouTube video using Selenium headless browser
    
    Args:
        video_id (str): YouTube video ID (e.g., "dQw4w9WgXcQ")
        
    Returns:
        list: List of transcript segments with text, start time, and duration
    """
    print(f"Attempting to get transcript for video ID: {video_id}")
    
    # Configure Chrome options for headless operation on a server
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    # Add a realistic user agent
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
    
    # Create the driver
    print("Initializing Chrome driver...")
    driver = webdriver.Chrome(options=options)
    
    try:
        # Load the YouTube video page
        url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"Navigating to {url}")
        driver.get(url)
        
        # Wait for the page to load
        time.sleep(3)
        
        # Execute JavaScript to extract caption data from the page
        print("Extracting captions data...")
        captions_data = driver.execute_script("""
            var ytInitialPlayerResponse = null;
            
            // Try to find the ytInitialPlayerResponse
            for (var script of document.scripts) {
                if (script.text.includes('ytInitialPlayerResponse')) {
                    try {
                        var match = script.text.match(/ytInitialPlayerResponse = (.+?});/);
                        if (match) {
                            ytInitialPlayerResponse = JSON.parse(match[1]);
                            break;
                        }
                    } catch (e) {
                        continue;
                    }
                }
            }
            
            if (!ytInitialPlayerResponse) {
                return {error: "Could not find ytInitialPlayerResponse"};
            }
            
            // Check if captions are available
            if (!ytInitialPlayerResponse.captions) {
                return {error: "No captions available for this video"};
            }
            
            // Get caption data
            var captionTracks = ytInitialPlayerResponse.captions.playerCaptionsTracklistRenderer.captionTracks;
            if (!captionTracks || captionTracks.length === 0) {
                return {error: "No caption tracks found"};
            }
            
            // Find English captions or use the first available caption track
            var captionTrack = null;
            for (var track of captionTracks) {
                if (track.languageCode === 'en') {
                    captionTrack = track;
                    break;
                }
            }
            
            if (!captionTrack) {
                captionTrack = captionTracks[0];
            }
            
            return {
                baseUrl: captionTrack.baseUrl,
                languageCode: captionTrack.languageCode,
                name: captionTrack.name.simpleText,
                isGenerated: captionTrack.kind === 'asr'
            };
        """)
        
        print("Caption data:", captions_data)
        
        if not captions_data or 'error' in captions_data:
            print(f"Error extracting captions: {captions_data.get('error', 'Unknown error')}")
            return None
        
        # Fetch the transcript data from the baseUrl
        print(f"Fetching transcript from URL: {captions_data['baseUrl']}")
        driver.get(captions_data['baseUrl'])
        
        # Get the XML content and parse it
        xml_content = driver.page_source
        print("Got XML response. Parsing transcript...")
        
        # Simple XML parsing to extract transcript (this is a basic implementation)
        # A more robust solution would use proper XML parsing libraries
        transcript_items = []
        text_elements = re.findall(r'<text start="([\d\.]+)" dur="([\d\.]+)">(.*?)</text>', xml_content)
        
        for start, duration, text in text_elements:
            # Clean HTML entities in text
            clean_text = text.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
            transcript_items.append({
                'text': clean_text,
                'start': float(start),
                'duration': float(duration)
            })
        
        print(f"Successfully extracted {len(transcript_items)} transcript segments")
        return transcript_items
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    
    finally:
        # Always close the driver
        print("Closing Chrome driver")
        driver.quit()

if __name__ == "__main__":
    # Test with a known video ID
    video_id = "dQw4w9WgXcQ"  # Rick Astley - Never Gonna Give You Up
    
    transcript = get_youtube_transcript(video_id)
    
    if transcript:
        print("\nTranscript sample (first 3 items):")
        for item in transcript[:3]:
            print(f"{item['start']:.2f} - {item['start'] + item['duration']:.2f}: {item['text']}")
        
        # Save full transcript to file
        with open('transcript.json', 'w', encoding='utf-8') as f:
            json.dump(transcript, f, indent=2)
        print(f"\nFull transcript saved to transcript.json ({len(transcript)} segments)")
    else:
        print("Failed to get transcript")