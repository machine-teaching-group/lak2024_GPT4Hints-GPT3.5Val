import sys
from typing import Dict, List, Optional

sys.path.append(".")

from src.utils.basicalgo_utils import (
    format_BasicAlgo_failing_testcase,
    format_BasicAlgo_problem_description,
    format_BasicAlgo_resources,
)


def make_starter_fix_prompt_messages(dataset: str, *args, **kwargs) -> List[Dict[str, str]]:
    """
    Form a prompt for a repair request.
    :param dataset:
    :param args:
    :param kwargs:
    :return: The prompt.
    """
    if dataset in {"DataAnalysis", "DataRegex"}:
        return make_starter_fix_prompt_messages_DS(*args, **kwargs)
    elif dataset == "BasicAlgo":
        return make_starter_fix_prompt_messages_BasicAlgo(*args, **kwargs)
    else:
        raise ValueError(f"Cannot make repair prompt for dataset {dataset}")


def make_starter_fix_prompt_messages_DS(
    instruction_phase: str,
    instruction_type: str,
    config,
    buggy_program: str,
    assignment_id: str,
    question_id: str,
    program_output: str,
    expected_output: str,
    generated_output: Optional[str] = None,
    **kwargs,
) -> List[Dict[str, str]]:
    if instruction_phase == "repair":
        command_head = config[instruction_phase]["command_head"]
        command_tail = config[instruction_phase]["command_tail"]["DS"]
        info_for_simstu_repair = ""
    else:  # simstu repair
        command_head = config[instruction_phase]["explanation"]["command_head"]
        command_tail = config[instruction_phase]["explanation"]["command_tail"]["DS"]
        info_for_simstu_repair = config["questions"]["all"]["generated_explanation"].format(
            generated_explanation=generated_output
        )
    prob_desc = config["questions"][f"a-{assignment_id}_q-{question_id}"]["problem_description"]
    resources = config["questions"][f"a-{assignment_id}_q-{question_id}"]["resources"]
    test_case = config["questions"]["all"]["test_case"].format(
        program_output=program_output, expected_output=expected_output
    )
    buggy = config["questions"]["all"]["buggy"].format(buggy_program=buggy_program)

    instruction_format = config["symbolic"][instruction_type]
    instruction = instruction_format.format(
        command_head=command_head,
        problem_description=prob_desc,
        resources=resources,
        test_case=test_case,
        buggy=buggy,
        generated_output=info_for_simstu_repair,
        command_tail=command_tail,
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruction},
    ]

    return messages


def make_starter_fix_prompt_messages_BasicAlgo(
    instruction_phase: str,
    instruction_type: str,
    config,
    buggy_program: str,
    question_id: str,
    failing_testcase: str,
    program_output: str,
    expected_output: str,
    generated_output: Optional[str] = None,
    **kwargs,
) -> List[Dict[str, str]]:
    if instruction_phase == "repair":
        command_head = config[instruction_phase]["command_head"]
        command_tail = config[instruction_phase]["command_tail"]["ip10"]
        info_for_simstu_repair = ""
    else:  # simstu repair
        command_head = config[instruction_phase]["explanation"]["command_head"]
        command_tail = config[instruction_phase]["explanation"]["command_tail"]["ip10"]
        info_for_simstu_repair = config["questions"]["all"]["generated_explanation"].format(
            generated_explanation=generated_output
        )
    prob_desc = format_BasicAlgo_problem_description(config=config, question_id=question_id)
    resources = format_BasicAlgo_resources(config=config, question_id=question_id)
    test_case = format_BasicAlgo_failing_testcase(
        failing_testcase=failing_testcase, program_output=program_output, expected_output=expected_output
    )
    buggy = config["questions"]["all"]["buggy"].format(buggy_program=buggy_program)

    instruction_format = config["symbolic"][instruction_type]
    instruction = instruction_format.format(
        command_head=command_head,
        problem_description=prob_desc,
        resources=resources,
        test_case=test_case,
        buggy=buggy,
        generated_output=info_for_simstu_repair,
        command_tail=command_tail,
    )

    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": instruction},
    ]

    return messages
