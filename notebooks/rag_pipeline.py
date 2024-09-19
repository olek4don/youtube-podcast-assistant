import json
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass


class OpenAIClient(LLMClient):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        import openai

        self.client = openai.ChatCompletion()
        self.model = model

    def generate(self, prompt: str) -> str:
        response = self.client.create(
            model=self.model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


class HuggingFaceClient(LLMClient):
    def __init__(self, model: str = "facebook/opt-350m"):
        from transformers import pipeline

        self.generator = pipeline("text-generation", model=model)

    def generate(self, prompt: str) -> str:
        response = self.generator(prompt, max_length=100, num_return_sequences=1)
        return response[0]["generated_text"]


def build_prompt(context: str, template: Optional[str] = None) -> str:
    default_template = """
    Generate a question and answer based on the following context:
    {context}
    Respond with a JSON object containing "question" and "answer" keys.
    If there's not enough information, use "NA" as the answer.
    """.strip()

    prompt_template = template or default_template
    return prompt_template.format(context=context).strip()


def rag(
    context: str, llm_client: LLMClient, template: Optional[str] = None
) -> Dict[str, Any]:
    prompt = build_prompt(context, template)
    response = llm_client.generate(prompt)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response", "raw_response": response}


# Example usage
if __name__ == "__main__":
    # Using OpenAI
    openai_client = OpenAIClient(model="gpt-3.5-turbo")
    result_openai = rag("Sample context about AI", openai_client)
    print("OpenAI result:", result_openai)

    # Using HuggingFace
    hf_client = HuggingFaceClient(model="facebook/opt-350m")
    result_hf = rag("Sample context about machine learning", hf_client)
    print("HuggingFace result:", result_hf)
