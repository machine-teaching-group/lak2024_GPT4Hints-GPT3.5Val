import json
import os
import time
from typing import Dict, Sequence

import openai

# Define the timestamp at which we can query LLM (again)
next_query_time = 0

# Cooldown time between queries
QUERY_COOLDOWN = 0.1
N_COOLDOWN = 0.1


def load_openai_api(pass_file: str = "~/.password.json", key: str = "openai-api-key") -> str:
    """Load the API from `~/.password.json`"""
    with open(os.path.expanduser(pass_file)) as f:
        content = json.load(f)
        api = content[key]
    return api


def ask_chatgpt(
    messages: Sequence[Dict[str, str]],
    model: str,
    n: int,
    temperature: float,
    presence_penalty=0,
    frequency_penalty=0,
    max_tolerant_invalid_requests: int = 5,
):
    """
    Function to query ChatGPT (and GPT-4) with handling of errors.
    """
    # Wait for cooldown
    global next_query_time
    while time.time() < next_query_time:
        time.sleep(next_query_time - time.time())

    cnt_invalid_requests = 0

    while True:
        try:
            # Query
            openai.api_key = api_key
            request_output = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                n=n,
                temperature=temperature,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
            )

            # Setup cooldown time
            next_query_time = time.time() + QUERY_COOLDOWN + n * N_COOLDOWN

            return request_output

        except openai.error.RateLimitError:
            print("Rate limited")
            time.sleep(15)
        except openai.error.Timeout:
            print("Timeout")
            time.sleep(10)
        except (openai.error.APIConnectionError, openai.error.APIError, openai.error.ServiceUnavailableError):
            time.sleep(60)
        except openai.error.InvalidRequestError as e:
            print(f"During calling `generate_feedback`, the following error occurs: {e}")
            cnt_invalid_requests += 1
            if cnt_invalid_requests > max_tolerant_invalid_requests:
                return []
        except KeyError:
            pass


# Load openai api
api_key = load_openai_api()
