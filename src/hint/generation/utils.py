import sys
from typing import Tuple

sys.path.append(".")


def extract_explanation_hint_from_response(text_response: str) -> Tuple[str, str]:
    """
    Given a text answer from LLMs, this function extract the explanation and hint from the answer.
    Extraction is done using a pre-defined format (i.e., explanation is preceded by `(1)` and hint is preceded by `(2)`.
    """
    explanation, hint = text_response.split("\n(2)")
    if explanation.startswith("(1)"):
        explanation = explanation[len("(1)") :]
    explanation = explanation.strip()
    hint = hint.strip()

    return explanation, hint
