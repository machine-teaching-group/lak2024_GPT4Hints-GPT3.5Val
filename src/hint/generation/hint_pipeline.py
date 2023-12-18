import sys
from typing import Tuple

sys.path.append(".")

from src.hint.generation.generate_feedback import generate_feedback
from src.hint.generation.make_prompt import make_starter_hint_prompt_messages
from src.hint.generation.utils import extract_explanation_hint_from_response
from src.repair.evaluation.metrics import get_buggy_output


def feedback(
    config,
    buggy_program: str,
    fixed_program: str,
    dataset: str,
    question_id: str,
) -> Tuple[str, str]:
    # Pre-check some arguments
    if buggy_program.strip() == "":
        raise ValueError("Buggy program cannot be empty.")
    if dataset not in {"DataAnalysis", "DataRegex", "BasicAlgo"}:
        raise ValueError("Dataset not supported. We only support 'DataAnalysis', 'DataRegex', and 'BasicAlgo'.")
    if dataset in {"DataAnalysis", "DataRegex"} and question_id != "2":
        raise ValueError(f"For dataset '{dataset}', please leave question_id as default.")
    if dataset == "BasicAlgo" and question_id.lower() not in {
        "gcd",
        "fibonacci",
        "divisorsdiv3",
        "palindrome",
        "mergestrs",
    }:
        raise ValueError(
            f"For dataset {dataset}, we only support question_id: \
        'gcd', 'fibonacci', 'divisorsdiv3', 'palindrome', 'mergestrs'"
        )

    # Deduce and extract some metadata
    if dataset in {"DataAnalysis", "DataRegex"}:
        if dataset == "DataRegex":
            assignment_id = "1"
        else:
            assignment_id = "2"
        test_script = config["questions"].get(f"a-{assignment_id}_q-{question_id}", {}).get("test_script", None)
        expected_output = config["questions"][f"a-{assignment_id}_q-{question_id}"]["expected_output"]
        testcases_folder = None
        driver_code = None
    else:  # dataset == "BasicAlgo"
        assignment_id = "ip10"
        test_script = None
        expected_output = None
        testcases_folder = config["questions"][f"a-ip10_q-{question_id}"]["testcases_path"]
        driver_code = config["questions"][f"a-ip10_q-{question_id}"]["driver_code"]
    failing_testcase, program_output, expected_output = get_buggy_output(
        dataset=dataset,
        input_program=buggy_program,
        test_script=test_script,
        expected_output=expected_output,
        testcases_folder=testcases_folder,
        driver_code=driver_code,
    )

    # Form the feedback prompt
    feedback_prompt_messages = make_starter_hint_prompt_messages(
        dataset=dataset,
        buggy_program=buggy_program,
        config=config,
        assignment_id=assignment_id,
        question_id=question_id,
        program_output=program_output,
        expected_output=expected_output,
        failing_testcase=failing_testcase,
        repair_program=fixed_program,
    )

    _, text_response = generate_feedback(
        hint_messages=feedback_prompt_messages,
    )

    explanation, hint = extract_explanation_hint_from_response(text_response=text_response)

    return explanation, hint
