from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import os
from .formatter import *
import json

def get_youtube_video_urls(query, max_results=5):
    api_key = os.getenv("GOOGLEAPIKEY")  # Replace with your actual API key
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.search().list(
        part='snippet',
        q=query + 'review',
        maxResults=max_results,
        type='video',
        relevanceLanguage='en',  # Filter by English language
        videoCaption='closedCaption'  # Filter by videos with closed captions
    )
    response = request.execute()

    video_info_list = []
    video_urls = []
    for item in response['items']:
        video_id = item['id']['videoId']
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        video_urls.append(video_url)
        snippet = item['snippet']
        video_info = {
        "title": snippet['title'],
        "author": snippet['channelTitle'],
        "videoId": item['id']['videoId']
        }
        video_info_list.append(video_info)

    return video_urls, video_info_list


def get_captions(video_id, language_code='en'):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language_code])
        captions = " ".join([entry['text'] for entry in transcript])
        return captions
    except Exception as e:
        return f"An error occurred: {str(e)}"


def review(phoneModel):
    # Example usage:
    captionsList = []
    video_urls, video_info = get_youtube_video_urls(phoneModel)
    # print(phoneModel)

    for url in video_urls:
        video_id = url.split('v=')[1]
        caption = get_captions(video_id, language_code='en')
        print(caption)
        print()
        captionsList.append(caption)

    
    phone_review = {
    "title": "Phone_name Review",
    "shortDescription": "A short description of the Phone_name",
    "Camera Quality": [
            "list of points describing the details"
        ],
    "Battery Life": [
            "list of points describing the details"
        ],
    "Performance": [
            "list of points describing the details"
        ],
    "Build Quality": [
            "list of points describing the details"
        ],
    "Display": [
            "list of points describing the details"
        ],
    "Pros": [
            "list of points describing the details"
        ],
    "Cons": [
            "list of points describing the details"
        ],

    "Overall": "overall review of the phone"
}
    
    text_prompt = f"""
    You are a professional reviewer of mobiles and your task is to summarize the reviews of a phone model based on the captions from the top 5 YouTube review videos. Here are the captions from the videos:

    Video 1: {captionsList[0]}
    Video 2: {captionsList[1]}
    Video 3: {captionsList[2]}
    Video 4: {captionsList[3]}
    Video 5: {captionsList[4]}

Please write an overall review of the phone, summarizing the main points discussed in these videos. Your review should include:

1. A title with the phone name as heading
2. A brief introduction about the phone without any symbols.
3. A summary of the key features and performance aspects, highlighting the pros and cons in form of subtopics.
4. Citations in parentheses after each point indicating which video(s) the point was mentioned in (e.g., (1), (2), (3), etc.).

Ensure the review is concise, well-structured, and clearly references the videos for each point made. Here is an format for the review:

The response should only be a json format in this format:
{phone_review}
"""

    GEMMA_API=os.getenv("GEMINISTUDIOKEY")
    genai.configure(api_key=GEMMA_API)
    model = genai.GenerativeModel('gemini-1.5-flash', 
                                  generation_config={"response_mime_type" : "application/json"}
                                  )
    response = model.generate_content(text_prompt)
    print(is_valid_json(response.text))
    print(response.text)
    return response, video_info

def is_valid_json(input_string):
    try:
        json.loads(input_string)
        return True
    except json.JSONDecodeError:
        return False

# generated_review, video_info = review("samsung s22 fe")

# print(is_valid_json(generated_review.text))

# input_data= json.loads(generated_review.text)
# x = restructure_data(input_data , video_info)

# print(x)
