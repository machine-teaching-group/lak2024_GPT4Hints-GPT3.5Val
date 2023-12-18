import sys
from typing import Dict, Sequence

sys.path.append(".")

from src.utils.openai_utils import ask_chatgpt


def generate_feedback(
    hint_messages: Sequence[Dict[str, str]],
):
    """
    Generate feedback using LLMs with the input parameters.
    """

    request_output = ask_chatgpt(messages=hint_messages, n=1, temperature=0, model="gpt-4")

    for choice in request_output["choices"]:
        if "message" in choice and "content" in choice["message"]:
            llm_hint = choice["message"]["content"]
            hint = llm_hint
        else:
            print("LLM outputs an error")
            hint = None

    return request_output, hint
