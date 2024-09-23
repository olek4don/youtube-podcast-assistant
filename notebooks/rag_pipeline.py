# %%
import json
import requests
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI()
# Load environment variables from a .env file
load_dotenv()

# Set the OpenAI API key environment variable
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
###############################################################


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Abstract method to generate a response based on the given prompt.

        Args:
            prompt (str): The input prompt to generate a response for.

        Returns:
            str: The generated response.
        """
        pass


class OpenAIClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=256,
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return ""


class OllamaClient(LLMClient):

    def __init__(self, model: str = "llama2:7b"):
        self.model = model
        self.api_url = "http://localhost:11434/api/generate"

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": f"[INST] {prompt} [/INST]",
            "stream": False,
        }
        try:
            response = requests.post(self.api_url, json=payload)
            response.raise_for_status()  # This will raise an HTTPError for bad responses
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"Error making request to Ollama API: {e}")
            print(f"Response content: {response.text if response else 'No response'}")
            raise Exception(f"Ollama API error: {e}")


# class HuggingFaceClient(LLMClient):

#     def __init__(self, model: str = "meta-llama/Meta-Llama-3-8B"):

#         from transformers import pipeline

#         self.generator = pipeline("text-generation", model=model)

#     def generate(self, prompt: str) -> str:
#         response = self.generator(prompt, max_length=100, num_return_sequences=1)
#         return response[0]["generated_text"]


# %%
# def build_prompt(context: str, template: Optional[str] = None) -> str:
#     default_template = """
#     Generate an answer based on the following context and question:
#     {context}
#     Respond with a JSON object containing "question" and "answer" keys.
#     If there's not enough information, use "NA" as the answer.
#     """.strip()

#     prompt_template = template or default_template
#     return prompt_template.format(context=context).strip()


def build_prompt(
    query: str, search_results: List[Dict], template: Optional[str] = None
):
    prompt_template = """
    Generate a question based on the following context:
    CONTEXT:{context}
    Respond with a JSON object containing "answer" key.
    If there's not enough information, use "NA" as the answer.
    """.strip()

    context = ""

    for doc in search_results:
        context = context + f"text: {doc['text']}\nquestion: {doc['question']}\n\n"

    prompt = (
        template.format(question=query, context=context).strip()
        or prompt_template.format(question=query, context=context).strip()
    )
    return prompt


def rag(context: str, llm_client: LLMClient, template: Optional[str] = None) -> str:
    prompt = build_prompt(context, template)
    response = llm_client.generate(prompt)
    # return json.loads(response)
    return response


# %%
# Using Ollama
ollama_client = OllamaClient()
# try:
#     result_ollama = rag("Sample context about AI", ollama_client)
#     print("Ollama result:", result_ollama)
# except Exception as e:
#     print(f"An error occurred: {e}")
#     # Additional debugging information
#     print("Available Ollama models:")
#     os.system("ollama list")


# %%
from typing import List, Dict
import concurrent.futures
from tqdm import tqdm


def generate_answers(dataset: List[Dict], llm_client: LLMClient) -> List[Dict]:
    def process_item(item):
        context = item["text"]
        question = item["question"]
        template = f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
        answer = rag(context, llm_client, template)
        item["answer"] = answer
        return item

    total_items = len(dataset)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(
            tqdm(
                executor.map(process_item, dataset),
                total=total_items,
                desc="Generating Answers",
                unit="item",
            )
        )

    return results


# def generate_answers(dataset: List[Dict], llm_client: LLMClient) -> List[Dict]:
#     def process_item(item):
#         context = item["text"]
#         question = item["question"]
#         template = f"Generate answer based on following context and question: Context: {context}\n\nQuestion: {question}\n\nAnswer:"
#         answer = rag(context, llm_client, template)
#         item["answer"] = answer
#         return item

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         results = list(executor.map(process_item, dataset))

#     return results


# %%
with open("../data/external/transcript_qna_parsed.json", "r") as f:
    data = json.load(f)
# %%
import minsearch
import pandas as pd

df = pd.read_json("../data/external/transcript_qna_parsed.json")
# print(df)
df.to_csv("../data/external/transcript_qna_parsed.csv")

# %%
processed_dataset = generate_answers(data, ollama_client)
# %%
# Using OpenAI
openai_client = OpenAIClient(api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")
result_openai = rag("Sample context about AI", openai_client)
print("OpenAI result:", result_openai)
