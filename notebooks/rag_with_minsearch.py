# %%
import json
import requests

from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
from openai import OpenAI
from dotenv import load_dotenv

client = OpenAI()
# Load environment variables from a .env file
load_dotenv()


# %%
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


# %%
import pandas as pd
import minsearch

# convert to csv
# documents = df.to_dict(orient="records")

# %%
new_df = pd.read_csv("output.csv")
# %%
df_dict = new_df.to_dict(orient="records")
print(type(df_dict))
# %%

index = minsearch.Index(
    text_fields=["podcast_name", "text", "start", "question", "answer"],
    keyword_fields=[],
)
# %%
new_df.columns.str.lower()
# %%
new_df = new_df.fillna("")
# %%

index.fit(new_df.to_dict(orient="records"))


# %%
def build_prompt(
    query: str, search_results: List[Dict], template: Optional[str] = None
):
    prompt_template = """
    Generate a question based on the following context:
    CONTEXT:{context}
    If there's not enough information, use "NA" as the answer.
    """.strip()

    context = ""

    for doc in search_results:
        context = context + f"text: {doc['text']}\nquestion: {doc['question']}\n\n"

    prompt = template or prompt_template.format(question=query, context=context).strip()
    return prompt


def rag(context: str, llm_client: LLMClient, template: Optional[str] = None) -> str:

    prompt = build_prompt(context, template)
    response = llm_client.generate(prompt)
    # return json.loads(response)
    return response


# %%
