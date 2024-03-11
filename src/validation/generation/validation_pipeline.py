import sys

sys.path.append(".")

from src.repair.generation.repair_pipeline import repair


def validate(
    config,
    buggy_program: str,
    explanation: str,
    dataset: str,
    question_id: str,
) -> bool:
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

    # Get number of successful repairs using the standard prompt
    _, correct_repairs_standard = repair(
        instruction_phase="repair",
        config=config,
        buggy_program=buggy_program,
        dataset=dataset,
        question_id=question_id,
        model="gpt-3.5-turbo",
        generated_output=None,
    )
    n1 = len(correct_repairs_standard)

    # Get number of successful repairs using the augmented prompt
    _, correct_repairs_augmented = repair(
        instruction_phase="simstu_repair",
        config=config,
        buggy_program=buggy_program,
        dataset=dataset,
        question_id=question_id,
        model="gpt-3.5-turbo",
        generated_output=explanation,
    )
    n2 = len(correct_repairs_augmented)

    # Compute validation result
    n, alpha, beta = 10, 0.5, 0.25
    eps = 1e-9  # epsilon for float comparison
    if (n2 >= n1 - eps) and ((n2 / n >= alpha - eps) or (n2 / n - n1 / n >= beta - eps)):
        validation_result = True
    else:
        validation_result = False

    return validation_result
