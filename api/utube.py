import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import json

# Set up Google Gemini API key from environment variables
import os
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_youtube_transcript(video_id):
    """Fetches transcript from YouTube."""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def summarize_text(text):
    """Summarizes text using Google's Gemini AI."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize this YouTube transcript in a concise and informative manner:\n\n{text}")
    return response.text

# Vercel handler
def handler(request):
    body = request.get_json()
    video_url = body.get("url", "")
    video_id = video_url.split("v=")[-1] if "v=" in video_url else video_url.split("/")[-1]

    try:
        transcript = get_youtube_transcript(video_id)
        if "Error" in transcript:
            return json.dumps({"error": transcript})
        
        summary = summarize_text(transcript)
        return json.dumps({"summary": summary})
    except Exception as e:
        return json.dumps({"error": str(e)})