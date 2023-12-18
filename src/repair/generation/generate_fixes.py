import dataclasses
import re
import sys
from typing import Dict, Optional, Sequence

sys.path.append(".")

from src.repair.generation.preprocess import strip_program
from src.utils.openai_utils import ask_chatgpt


@dataclasses.dataclass
class FixObject:
    """Class to store LLMs' answers for repair requests."""

    response_message: Optional[str]
    fixed_program: Optional[str]

    def __str__(self):
        return str(self.to_dict())

    def to_dict(self):
        return {
            "response_message": self.response_message,
            "fixed_program": self.fixed_program,
        }


def generate_fixes(
    repair_messages: Sequence[Dict[str, str]],
    model: str,
):
    """
    Generate multiple fixes using LLMs with the input parameters.
    """

    fix_objects = []
    request_output = ask_chatgpt(
        messages=repair_messages,
        n=10,
        temperature=0.5,
        model=model,
    )

    for choice in request_output["choices"]:
        if "message" in choice and "content" in choice["message"]:
            llm_answer = choice["message"]["content"]
            llm_fix = extract_fixed_program(llm_answer)
            fix_objects.append(FixObject(response_message=llm_answer, fixed_program=llm_fix))
        else:
            print("LLM outputs an error")
            fix_objects.append(FixObject(None, None))

    return request_output, fix_objects


def extract_fixed_program(llm_answer: str):
    """
    Extract the fixed program from the answer of the LLM.
    The fixed program is assumed to be the longest piece of code (enclosed by two ```) in the answer.
    :param llm_answer:
    :return: str, the fixed program
    """
    boundary = "```"  # separate code and text
    bound_places = [m.start() for m in re.finditer(boundary, llm_answer)]

    longest_code = ""

    for i in range(0, len(bound_places), 2):
        code_start_pos = bound_places[i] + 3
        if i + 1 < len(bound_places):
            code_end_pos = bound_places[i + 1]
        else:  # if there is no ending boundary, we assume the code stretch until the end of the answer
            code_end_pos = len(llm_answer)

        code = llm_answer[code_start_pos:code_end_pos]
        if code.startswith("python\n"):
            code = code[7:]  # remove "python\n"

        if len(code) > len(longest_code):
            longest_code = code

    longest_code = strip_program(longest_code)

    return longest_code
