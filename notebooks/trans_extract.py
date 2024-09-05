# %%
import os
import json
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import is_torch_tpu_available

# Expand the ~ to the user's home directory
file_path = os.path.expanduser(
    "../data/external/transcript.json"
)
video_id = "Kbk9BiPhm7o"
podcast_name = "Elon Musk: Neuralink and the Future of Humanity | Lex Fridman Podcast"

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

transcript = get_transcript(video_id)


def convert_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def process_transcript(data, podcast_name: str):
    merged_data = []
    batch_size = 20

    for i in range(0, len(data), batch_size):
        batch = data[i : i + batch_size]
        merged_dict = {
            "podcast_name": podcast_name,
            "text": " ".join([d["text"] for d in batch]),
            "start": convert_time(int(batch[0]["start"])),
        }
        merged_data.append(merged_dict)

    return merged_data

# %%
%pip install --upgrade --quiet  youtube-transcript-api

# %%
!pip install --upgrade langchain

# %%
from langchain.document_loaders.youtube import TranscriptFormat
from langchain.document_loaders import YoutubeLoader

loader = YoutubeLoader.from_youtube_url(
    "https://www.youtube.com/watch?v=Kbk9BiPhm7o",
    add_video_info=True,
    transcript_format=TranscriptFormat.CHUNKS,
    chunk_size_seconds=30,
)
print("\n\n".join(map(repr, loader.load())))

# %%
modified_transcript = process_transcript(transcript, podcast_name)

# %%
len(modified_transcript)

# %%
# Write to the file
with open(file_path, "w") as f:
    json.dump(modified_transcript, f, indent=4, ensure_ascii=False)


# %%
!head ../data/external/transcript.json

# %%



