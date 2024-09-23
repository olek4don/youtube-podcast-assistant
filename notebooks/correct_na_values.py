# %%
from openai import openai
from dotenv import load_dotenv
import json
from typing import dict, any, optional

client = openai()
# load environment variables from a .env file
load_dotenv()

# set the openai api key environment variable
# os.environ["openai_api_key"] = os.getenv("openai_api_key")


# %%

with open("../data/external/transcript_qna.json", "r") as f:
    to_replace = json.load(f)


# %%
def llm(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def rag(context: str, template: optional[str] = none):
    prompt = build_prompt(context, template)
    answer = llm(prompt)
    return answer


def add_qa_to_transcripts(transcripts):
    """add a "question" and "answer" prepared by llm to each transcript in the list of transcripts"""
    new_transcripts = []
    for transcript in transcripts:
        new_qa = rag(transcript["text"])
        new_transcript = {**transcript, **new_qa}
        new_transcripts.append(new_transcript)
    return new_transcripts


# %%
def build_prompt(context: str, template: optional[str] = none) -> str:
    if template is none:
        template = """you are a proffesional podcast assistant creating a test for advanced listeners. for each context, create a question that is specific to the context. only ask questions that can be answered using the context. avoid creating generic or general questions.

    format the output as json that can be directly parsed using json.loads().
    don't use any markdown or html formatting in your response.
    answer pattern:
    {{"question": question}}

    context: {context}""".strip()

    prompt = template.format(context=context).strip()

    return prompt


answer_prompt_template = """you are a proffesional podcast assistant creating a test for advanced listeners. for each question and context, create a answer for the question that is specific to the context. only answer using the context. avoid creating generic or general answers.

format the output as json that can be directly parsed using json.loads().
don't use any markdown or html formatting in your response.
answer pattern:
{{"answer": answer}}

context: 
{context}""".strip()


# %%
transcripts_with_qa = add_qa_to_transcripts(transcripts)
for t in transcripts_with_qa:
    print(json.dumps(t, indent=4), end="\n\n")

# %%
with open("../data/external/transcript_qna_parsed.json", "r") as f:
    data = json.load(f)


def update_q(data):
    for d in data:
        if d["answer"] == "na":
            context = d["text"]
            new_question = json.loads(rag(context))
            print(new_question)
            d["question"] = new_question["question"]
            print(d)
    return data


def update_a(data):
    entry_template = """
    text: {text} \n
    question: {question}
    """.strip()
    context = ""
    for d in data:
        if d["answer"] == "na":
            context = entry_template.format(**d)
            # print(context, end="\n ----- \n")
            # print(build_prompt(context, answer_prompt_template), end="\n ----- \n")
            new_answer = json.loads(rag(context, answer_prompt_template))
            # print(new_answer, end="\n ----- \n")
            d["answer"] = new_answer["answer"]
            # print(d, end="\n ----- \n")
    return data


# %%
# new_question_list = update_qa(data)
new_data = update_q(data)

# %%
new_final_data = update_a(new_data)
# %%
with open("../data/external/final_transcript_qna.json", "w") as f:
    json.dump(new_final_data, f, indent=4)

# %%
# add last qa prepared directly in ChatGPT site to complete the transcript
with open("../data/external/final_transcript_qna.json", "r") as f:
    data = json.load(f)
for d in data:
    if d["start"] == "01:00:50":
        d["question"] = (
            "Why does Elon Musk express concern about AI being programmed to lie, even in small ways?"
        )
        d["answer"] = (
            "Elon Musk expresses concern about AI being programmed to lie, even in small ways, because small lies can escalate into larger ones, particularly when deployed at scale by humans."
        )
# %%
with open("../data/external/final_transcript_qna.json", "w") as f:
    json.dump(data, f, indent=4)

# # find the dictionaries in data that have "na" as a value
# na_dicts = [d for d in data if "na" in d.values()]

# # find the dictionaries in new_final_data that have the same "start" values as the dictionaries in na_dicts
# matching_dicts = [
#     d for d in new_final_data if d.get("start") in [d.get("start") for d in na_dicts]
# ]

# print(na_dicts, end="\n\n")
# print(matching_dicts)
