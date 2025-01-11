import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
import os
import json


# Configure the Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_text = " ".join([entry['text'] for entry in transcript])
        return full_text
    except Exception as e:
        return f"Error fetching transcript: {str(e)}"

def summarize_text(text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Summarize this YouTube transcript in a concise and informative manner:\n\n{text}")
    return response.text

def handler(request):
    # Extract JSON from the request body
    body = request.get_json()

    # Get the video URL from the body
    video_url = body.get("url", "")
    if not video_url:
        return json.dumps({"error": "No YouTube URL provided"})

    # Extract video ID from URL
    video_id = video_url.split("v=")[-1] if "v=" in video_url else video_url.split("/")[-1]

    try:
        # Get YouTube transcript
        transcript = get_youtube_transcript(video_id)
        if "Error" in transcript:
            return json.dumps({"error": transcript})

        # Generate summary of the transcript
        summary = summarize_text(transcript)
        return json.dumps({"summary": summary})

    except Exception as e:
        return json.dumps({"error": str(e)})
