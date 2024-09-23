# %%
from openai import OpenAI
from dotenv import load_dotenv
import json
import re

client = OpenAI()
# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# %%
with open("../data/external/test_transcript.json") as f:
    test_transcripts = json.load(f)


print(test_transcripts[0])


# %%
def build_prompt(context: str) -> str:
    prompt_template = """
    You're a professional podcast assistant. You will generate QUESTION and ANSWER based on the CONTEXT from text-chunks of the transcript.
    Here you will generate a QUESTION for which the CONTEXT is relevant.
    The output should be valid JSON, with keys enclosed in double quotes and properly escaped characters.
    Respond only with a valid JSON object containing the keys "question" and "answer".
    Do not include any markup formatting or code block syntax.
    Avoid to including word "context" in the question or answer.
    Pattern:
    {{"question": QUESTION, "answer": ANSWER}}
    If the text does not contain sufficient information to answer the question, do not make up information and give the answer as "NA".
    You are only allowed to answer questions related to CONTEXT.
    Use only the facts from the CONTEXT when answering the QUESTION.
    Remember that the text chunks derive from podcast where podcaster talks with the guest, so if you see diversity of roles in the CONTEXT, try to recognize that.
    Focus.
    CONTEXT: 
    {context}
    """.strip()

    prompt = prompt_template.format(context=context).strip()
    return prompt


def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def rag(context: str):
    prompt = build_prompt(context)
    answer = llm(prompt)
    return json.loads(answer)


def add_qa_to_transcripts(transcripts):
    """Add a "question" and "answer" prepared by llm to each transcript in the list of transcripts"""
    new_transcripts = []
    for transcript in transcripts:
        new_qa = rag(transcript["text"])
        new_transcript = {**transcript, **new_qa}
        new_transcripts.append(new_transcript)
    return new_transcripts


# %%
test_transcript = test_transcripts[0]["text"]

test_rag = rag(test_transcript)
# %%
transcripts_with_qa = add_qa_to_transcripts(transcripts)
for t in transcripts_with_qa:
    print(json.dumps(t, indent=4), end="\n\n")

# %%

with open("../data/external/transcript_qna.json", "r") as f:
    to_replace = json.load(f)


# %%
# Function to replace variants of a word
def replace_word(text, target_words, replacement_word):
    # Use regular expression to replace any variant of the target word
    pattern = "|".join(re.escape(word) for word in target_words)
    return re.sub(
        r"" + pattern + r"(?=[\s]|$)", replacement_word, text, flags=re.IGNORECASE
    )


target_words = ["speaker", "the speaker", "speaker's"]

# Lists of guests and times
guests = ["Elon Musk", "DJ Seo", "Matthew McDougall", "Bliss Chapman", "Noland Arbaugh"]
starts = ["00:00:00", "01:27:34", "03:38:39", "05:06:01", "06:48:53"]

# zip both lists
guest_time = [{k: v} for k, v in zip(starts, guests)]
print(guest_time)

# %%
d_guest_time = dict(zip(starts, guests))
print(d_guest_time)
# %%


# # Initialize the current guest to None
current_guest = None

# Iterate over the transcript_qna
for item in to_replace:
    # change guest if new guest has appeared in the podcast
    for d in guest_time:
        for k, v in d.items():
            if item["start"] == k:
                current_guest = v

    # If a guest has appeared, replace variants of the word "speaker" with the current guest's name
    if current_guest:
        item["question"] = replace_word(item["question"], target_words, current_guest)
        item["answer"] = replace_word(item["answer"], target_words, current_guest)
# %%


def replace_speaker_with_guest(transcript_qna, starts, guests, target_words):
    """
    Replace variants of the word "speaker" with the current guest's name in the transcript_qna.

    Args:
        transcript_qna (list): List of transcript qna items.
        starts (list): List of start times for each guest.
        guests (list): List of guest names.
        target_words (list): List of words to replace (e.g. "speaker", "the speaker", etc.)

    Returns:
        list: Modified transcript_qna with replaced speaker names.
    """
    guest_time = dict(zip(starts, guests))
    current_guest = None
    for item in transcript_qna:
        # change guest if new guest has appeared in the podcast
        if item["start"] in guest_time:
            current_guest = guest_time[item["start"]]
        # If a guest has appeared, replace variants of the word "speaker" with the current guest's nam
        if current_guest:
            item["question"] = replace_word(
                item["question"], target_words, current_guest
            )
            item["answer"] = replace_word(item["answer"], target_words, current_guest)

    return transcript_qna


# %%
with open("../data/external/transcript_qna_parsed.json", "r") as f:
    data = json.load(f)
# %%
from datasets import Dataset

dataset = Dataset.from_json("../data/external/transcript_qna_parsed.json")

print(dataset)

# %%
eval_dataset = dataset.to_pandas()
eval_dataset.head()
# # %%
# from pathlib import Path

# file_path = "../data/external/transcript_qna_parsed.json"
# data = json.loads(Path(file_path).read_text())
# # %%
# from langchain_community.document_loaders import JSONLoader
# loader = JSONLoader(
#     file_path="../data/external/transcript_qna_parsed.json",
#     jq_schema=".[]",
#     text_content=False,
#     json_lines=False,
# )

# data = loader.load()
