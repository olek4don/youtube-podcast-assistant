# %%
import json
import os

from youtube_transcript_api import YouTubeTranscriptApi


def get_transcript(video_id):
    try:
        # Retrieve the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


video_id = "Kbk9BiPhm7o"
transcript = get_transcript(video_id)

# Expand the ~ to the user's home directory
file_path = os.path.expanduser(
    "~/MyCode/youtube-podcast-assistant/data/external/transcript.json"
)

# Create directories if they don't exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)


# %%
def get_transcript(video_id):
    try:
        # Retrieve the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


video_i = "Kbk9BiPhm7o"
transcript = get_transcript(video_id)


def convert_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def process_transcript(data):
    merged_data = []
    batch_size = 10

    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        merged_dict = {
            "text": " ".join([d["text"] for d in batch]),
            "start": convert_time(int(batch[0]["start"])),
        }
        merged_data.append(merged_dict)

    return merged_data


transcript = process_transcript(transcript)

# %%
transcript[0:20]

# %%
# Write to the file
with open(file_path, "w") as f:
    json.dump(transcript, f, indent=4)
