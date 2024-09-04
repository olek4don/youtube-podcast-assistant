# %%
from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id):
    try:
        # Retrieve the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


# Example usage
video_id = "Kbk9BiPhm7o"
transcript = get_transcript(video_id)
if transcript:
    print(transcript)


# %%
import json

with open("data/external/transcript.json", "w") as f:
    json.dump(transcript, f)

# %%
