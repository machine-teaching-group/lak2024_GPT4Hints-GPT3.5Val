import sys
from typing import Optional

sys.path.append(".")

from src.utils.basicalgo_utils import (
    format_BasicAlgo_failing_testcase,
    format_BasicAlgo_problem_description,
    format_BasicAlgo_resources,
)


def make_starter_hint_prompt_messages(dataset: str, *args, **kwargs):
    """
    Form a prompt for a feedback-generation request.
    :param dataset:
    :param args:
    :param kwargs:
    :return: The prompt.
    """
    if dataset in {"DataAnalysis", "DataRegex"}:
        return make_starter_hint_prompt_messages_DS(*args, **kwargs)
    elif dataset == "BasicAlgo":
        return make_starter_hint_prompt_messages_BasicAlgo(*args, **kwargs)
    else:
        raise ValueError(f"Do not support dataset {dataset}")


def make_starter_hint_prompt_messages_DS(
    config,
    buggy_program: str,
    assignment_id: str,
    question_id: str,
    program_output: str,
    expected_output: str,
    repair_program: Optional[str],
    *args,
    **kwargs,
):
    instruction_type = "ChatGPT-repair-if-correct"
    command_head = config["hint"]["command_head"]
    command_tail = config["hint"]["command_tail"]
    prob_desc = config["questions"][f"a-{assignment_id}_q-{question_id}"]["problem_description"]
    resources = config["questions"][f"a-{assignment_id}_q-{question_id}"]["resources"]
    test_case = config["questions"]["all"]["test_case"].format(
        program_output=program_output, expected_output=expected_output
    )
    buggy = config["questions"]["all"]["buggy"].format(buggy_program=buggy_program)

    if repair_program is None:
        instruction_type = "output"

    repair = config["questions"]["all"]["repair"].format(repair_program=repair_program)

    instruction_format = config["symbolic"][instruction_type]

    instruction = instruction_format.format(
        command_head=command_head,
        problem_description=prob_desc,
        resources=resources,
        test_case=test_case,
        buggy=buggy,
        repair=repair,
        command_tail=command_tail,
        generated_output="",
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruction},
    ]

    return messages


def make_starter_hint_prompt_messages_BasicAlgo(
    config,
    buggy_program: str,
    question_id: str,
    failing_testcase: str,
    program_output: str,
    expected_output: str,
    repair_program: Optional[str],
    *args,
    **kwargs,
):
    instruction_type = "ChatGPT-repair-if-correct"
    command_head = config["hint"]["command_head"]
    command_tail = config["hint"]["command_tail"]
    prob_desc = format_BasicAlgo_problem_description(config=config, question_id=question_id)
    resources = format_BasicAlgo_resources(config=config, question_id=question_id)
    test_case = format_BasicAlgo_failing_testcase(
        failing_testcase=failing_testcase, program_output=program_output, expected_output=expected_output
    )
    buggy = config["questions"]["all"]["buggy"].format(buggy_program=buggy_program)

    if repair_program is None:
        instruction_type = "output"

    repair = config["questions"]["all"]["repair"].format(repair_program=repair_program)

    instruction_format = config["symbolic"][instruction_type]

    instruction = instruction_format.format(
        command_head=command_head,
        problem_description=prob_desc,
        resources=resources,
        test_case=test_case,
        buggy=buggy,
        repair=repair,
        command_tail=command_tail,
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruction},
    ]

    return messages
