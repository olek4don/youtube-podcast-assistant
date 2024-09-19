# %%
import json
import os

from youtube_transcript_api import YouTubeTranscriptApi

# Expand the ~ to the user's home directory
file_path = os.path.expanduser("../data/external/transcript.json")
video_id = "Kbk9BiPhm7o"
podcast_name = "Elon Musk: Neuralink and the Future of Humanity | Lex Fridman Podcast"

# Create directories if they don't exist
os.makedirs(os.path.dirname(file_path), exist_ok=True)


# %%
def get_transcript(video_id):
    try:
        # Retrieve the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en-US"])
        return transcript
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None


def convert_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def preprocess_transcript(data, podcast_name: str):
    merged_data = []
    batch_size = 30

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
transcript = get_transcript(video_id)
processed_transcript = preprocess_transcript(transcript, podcast_name)
# %%
for i in processed_transcript[25:50]:
    print(i, end="\n\n")

# %%
print(len(processed_transcript))
# %%
import time
from openai import OpenAI
from typing import Dict, List
from dotenv import load_dotenv

client = OpenAI()
# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


def clean_transcript_chunk(chunk: Dict[str, str]) -> Dict[str, str]:
    """
    Clean a single chunk of transcript using GPT-4o-mini. Isn't necessary if we are able to use `languages=["en-US"]` parameter in YouTubeTranscriptApi.get_transcript, cuz it gives well formatted text.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "Clean up this transcript chunk. Remove filler words, repetitions, and correct minor errors. Maintain the original meaning and add appropriate punctuation. Preserve the exact meaning and key information.",
            },
            {"role": "user", "content": chunk["text"]},
        ],
        temperature=0.3,  # Lower temperature for more consistent outputs
    )

    # Create a new chunk with the cleaned text
    cleaned_chunk = chunk.copy()
    cleaned_chunk["text"] = response.choices[0].message.content
    return cleaned_chunk


def clean_and_format_transcript(
    transcript_chunks: List[Dict[str, str]]
) -> List[Dict[str, str]]:
    """
    Clean and format the entire transcript by processing each chunk.
    """
    cleaned_output = []
    for chunk in transcript_chunks:
        cleaned_chunk = clean_transcript_chunk(chunk)
        formatted_chunk = {
            "podcast_name": podcast_name,
            "text": cleaned_chunk["text"],
            "start": cleaned_chunk["start"],
        }
        cleaned_output.append(formatted_chunk)
        time.sleep(1)  # To avoid hitting API rate limits. Adjust as needed.

    return cleaned_output


# %%

test_data = processed_transcript[0:5]

cleaned_transcripts = clean_and_format_transcript(test_data)

for chunk in cleaned_transcripts[0:50]:
    print(f"Start: {chunk['start']}")
    print(f"Text: {chunk['text']}")
    print(f"Podcast: {chunk['podcast_name']}")
    print("---")


# %%
for i in cleaned_transcripts[0:10]:
    print(i)

# %%

import pandas as pd

# Convert the list to a pandas DataFrame
df = pd.DataFrame(cleaned_transcripts)

# Now you can use the to_json method
df.to_json(file_path, orient="records", indent=4)

# %%
print(len(cleaned_transcripts))
