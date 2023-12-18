import argparse
import sys
from pathlib import Path
from typing import Optional

sys.path.append(".")

from src.hint.generation.hint_pipeline import feedback
from src.repair.generation.repair_pipeline import repair
from src.utils.IO_utils import load_json_file
from src.utils.program_utils import load_program
from src.validation.generation.validation_pipeline import validate


def end_to_end(
    config,
    buggy_program: str,
    dataset: str,
    question_id: str,
) -> Optional[str]:
    # Pre-check some params
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

    for trial_id in range(3):
        # print(f"=== TRIAL {trial_id + 1}: === \n")
        fixed_program = repair(
            instruction_phase="repair",
            config=config,
            buggy_program=buggy_program,
            dataset=dataset,
            question_id=question_id,
            model="gpt-4",
        )[0]
        # print(f"FIXED PROGRAM:\n`{fixed_program}`\n")

        explanation, hint = feedback(
            config=config,
            buggy_program=buggy_program,
            fixed_program=fixed_program,
            dataset=dataset,
            question_id=question_id,
        )
        # print(f"EXPLANATION: `{explanation}`")
        # print(f"HINT: `{hint}`\n\n")

        validation_result = validate(
            config=config,
            buggy_program=buggy_program,
            explanation=explanation,
            dataset=dataset,
            question_id=question_id,
        )
        # print(f"VALIDATION: `{validation_result}`\n")

        if validation_result:
            break

    return hint


def main(args):
    feedback = end_to_end(
        config=load_json_file(args.config_path),
        buggy_program=load_program(args.buggy_program_path),
        dataset=args.dataset,
        question_id=args.question_id,
    )

    print(f"FINAL FEEDBACK: `{feedback}`\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_path", type=Path, default="src/config.json", help="Path to the JSON config file.")
    parser.add_argument("--buggy_program_path", type=Path, help="Path to the buggy program.")
    parser.add_argument("--dataset", type=str, help="Dataset, e.g., DataAnalysis, DataRegex, BasicAlgo.")
    parser.add_argument("--question_id", type=str, default="2", help="Question, e.g., 1.")

    args = parser.parse_args()
    main(args)
