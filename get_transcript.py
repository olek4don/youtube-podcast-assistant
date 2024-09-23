import json
import sys

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter, TextFormatter

transcript = YouTubeTranscriptApi.get_transcript(sys.argv[1], languages=["en-US"])

if sys.argv[3] == "json":
    formatter = JSONFormatter()
elif sys.argv[3] == "text":
    formatter = TextFormatter()

formatted = formatter.format_transcript(transcript)


f = open(sys.argv[2] + ".txt", "w")
f.write(formatted)
f.close
