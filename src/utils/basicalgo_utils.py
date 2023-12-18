def format_BasicAlgo_problem_description(
    config,
    question_id: str,
):
    prob_desc = (
        config["questions"][f"a-ip10_q-{question_id}"]["problem_description"]
        + " "
        + config["questions"][f"a-ip10_q-{question_id}"]["your_task"]
        + "\n\n"
        + config["questions"][f"a-ip10_q-{question_id}"]["examples"]
    )
    return prob_desc


def format_BasicAlgo_resources(
    config,
    question_id: str,
):
    resources = (
        config["questions"][f"a-ip10_q-{question_id}"]["expected_time_complexity"]
        + "\n"
        + config["questions"][f"a-ip10_q-{question_id}"]["expected_auxiliary_space"]
        + "\n"
        + config["questions"][f"a-ip10_q-{question_id}"]["constraints"]
    )
    return resources


def format_BasicAlgo_failing_testcase(
    failing_testcase: str,
    program_output: str,
    expected_output: str,
):
    test_case = (
        f"Failing Test Case:\nFor Input: {failing_testcase}\n"
        f"Your Code's output is: {program_output}\n"
        f"It's Correct output is: {expected_output}"
    )
    return test_case
