import sys
from typing import Optional, Sequence, Tuple

sys.path.append(".")

from src.repair.evaluation.metrics import get_buggy_output
from src.repair.generation.generate_fixes import FixObject, generate_fixes
from src.repair.generation.make_prompt import make_starter_fix_prompt_messages
from src.repair.generation.select_best_fix import (
    filter_by_passing_test_cases,
    select_fix_by_ed,
)


def repair(
    instruction_phase: str,
    config,
    buggy_program: str,
    dataset: str,
    question_id: str,
    model: str,
    generated_output: Optional[str] = None,  # in case of simstu validation, this is the generated explanation
) -> Tuple[str, Sequence[FixObject]]:
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

    # Form the repair prompt
    repair_messages = make_starter_fix_prompt_messages(
        dataset,
        instruction_phase=instruction_phase,
        instruction_type="resources",
        config=config,
        buggy_program=buggy_program,
        assignment_id=assignment_id,
        question_id=question_id,
        program_output=program_output,
        expected_output=expected_output,
        failing_testcase=failing_testcase,
        generated_output=generated_output,
    )

    # Generate multiple fixes
    _, fix_objects = generate_fixes(
        repair_messages=repair_messages,
        model=model,
    )

    # Select the best fix
    correct_fix_objects = filter_by_passing_test_cases(
        dataset=dataset,
        fix_objects=fix_objects,
        test_script=test_script,  # for DataRegex and DataAnalysis data
        testcases_path=testcases_folder,  # for BasicAlgo data
        driver_code=driver_code,  # for BasicAlgo data
    )
    min_ed_fix_object = select_fix_by_ed(
        buggy_program=buggy_program,
        correct_fix_objects=correct_fix_objects,
    )

    # Return the best fix and the list of correct fixes
    return min_ed_fix_object.fixed_program, correct_fix_objects
