# %%
import json
import os
import re
import string
from collections import defaultdict
from pathlib import Path

import pandas as pd

""" trancript is a JSON file, I want to open it as a dictionary and create a dataframe to work with. """

transcript_file = Path(
    "/home/axel/MyCode/youtube-podcast-assistant/data/external/transcript.json"
)
if transcript_file.exists():
    with open(transcript_file, "r") as f:
        transcript = json.load(f)
else:
    raise FileNotFoundError(f"{transcript_file} does not exist")

# for transcript_dict in transcript:
#     df = pd.DataFrame.from_dict(transcript_dict, orient="index")
#     print(df)

# %%
from youtube_transcript_api import YouTubeTranscriptApi
