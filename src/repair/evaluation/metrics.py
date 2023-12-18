import subprocess
import sys
import time
from pathlib import Path
from typing import Optional, Tuple

sys.path.append(".")

from src.utils.IO_utils import load_file, write_to_file

ROOT_PATH = Path(".").resolve()
tmp_folder = ROOT_PATH / "src/utils/sandbox/tmp_folder"


# Paths and Constants for DataRegex and DataAnalysis data
docker_output_local_folder_DS = ROOT_PATH / "src/utils/sandbox/docker_DS/output/"
docker_script_template_DS = r"""
docker run --rm \
-v {local_output_folder}:/usr/src/app/output \
-v {local_program_path}:/usr/src/app/{prog_name} \
-v {test_script}:/usr/src/app/tests.py \
datascience-docker python sandboxed_test_DS.py ./{prog_name} ./tests.py
"""

# Paths and Constants for BasicAlgo data
docker_output_local_folder_BasicAlgo = ROOT_PATH / "src/utils/sandbox/docker_BasicAlgo/output/"
docker_script_template_BasicAlgo = r"""
docker run --rm \
-v {local_output_folder}:/usr/src/app/output \
-v {local_program_path}:/usr/src/app/{prog_name} \
-v {testcases_folder}:/usr/src/app/testcases \
basicalgo-docker python sandboxed_test_BasicAlgo.py ./{prog_name}
"""


def pass_all_test_cases(dataset: str, *args, **kwargs) -> bool:
    """
    Run through all test cases to check whether the program is correct.
    """
    if dataset in {"DataAnalysis", "DataRegex"}:
        return pass_all_test_cases_DS(*args, **kwargs)[0]
    elif dataset == "BasicAlgo":
        return pass_all_test_cases_BasicAlgo(*args, **kwargs)[0]
    else:
        raise ValueError(f"Do not support dataset {dataset}")


def get_buggy_output(dataset: str, *args, **kwargs):
    """
    Run through all test cases to get the first failing test case (if any).
    """
    if dataset in {"DataAnalysis", "DataRegex"}:
        verdict, failing_case, buggy_output, expected_output = pass_all_test_cases_DS(*args, **kwargs)
    elif dataset == "BasicAlgo":
        verdict, failing_case, buggy_output, expected_output = pass_all_test_cases_BasicAlgo(*args, **kwargs)
    else:
        raise ValueError(f"Do not support dataset {dataset}")

    if verdict:
        failing_case = buggy_output = expected_output = ""
    return failing_case, buggy_output, expected_output


def pass_all_test_cases_DS(
    input_program: str, test_script: str, expected_output: Optional[str] = None, *args, **kwargs
) -> Tuple[bool, str, str, str]:
    """
    Given a program that attempts to solve a Data Science problem, test for its correctness.
    :param input_program:
    :param test_script:
    :param expected_output:
    :param args:
    :param kwargs:
    :return: A boolean for the correctness of the program,
             The failing case (since there is only 1 test case, we always return an empty string),
             The buggy output by the program for this failing test case (empty string if the program is correct),
             The expected output for this failing test case (empty string if the program is correct).
    """
    test_script = Path(test_script).resolve().as_posix()

    # write the program into a temporary file
    tmp_program_name = f"fix-{time.time()}.py"
    tmp_program_path = tmp_folder / tmp_program_name
    tmp_program_path.unlink(missing_ok=True)
    output_file_path = docker_output_local_folder_DS / tmp_program_name
    output_file_path.unlink(missing_ok=True)
    write_to_file(tmp_program_path, input_program)

    # invoke Docker and test the program
    docker_script = docker_script_template_DS.format(
        prog_name=tmp_program_name,
        local_output_folder=docker_output_local_folder_DS,
        local_program_path=tmp_program_path,
        test_script=test_script,
    )
    subprocess.run(docker_script, shell=True)

    # read the output and get the test-result
    test_output = load_file(output_file_path)
    result = test_output.startswith("True")
    buggy_output = test_output[test_output.find("BUGGY OUTPUT:") + len("BUGGY OUTPUT:") :].strip()

    # remove the temporary files
    tmp_program_path.unlink()
    output_file_path.unlink()

    return result, "", buggy_output, expected_output


def pass_all_test_cases_BasicAlgo(
    input_program: str, testcases_folder: str, driver_code: str, *args, **kwargs
) -> Tuple[bool, str, str, str]:
    """
    Given a program that attempts to solve a Basic Algorithms problem, test for its correctness.
    :param input_program:
    :param testcases_folder:
    :param driver_code:
    :param args:
    :param kwargs:
    :return: A boolean for the correctness of the program,
             The failing case (if any),
             The buggy output by the program for this failing test case (empty string if the program is correct),
             The expected output for this failing test case (empty string if the program is correct).
    """
    testcases_folder = Path(testcases_folder).resolve().as_posix()

    for added_code in ["", driver_code]:
        # write the program into a temporary file
        tmp_program_name = f"fix-{time.time()}.py"
        tmp_program_path = tmp_folder / tmp_program_name
        tmp_program_path.unlink(missing_ok=True)
        output_file_path = docker_output_local_folder_BasicAlgo / tmp_program_name
        output_file_path.unlink(missing_ok=True)
        repaired_program_postprocessed = input_program + "\n\n" + added_code
        write_to_file(tmp_program_path, repaired_program_postprocessed)

        # invoke Docker and test the program
        docker_script = docker_script_template_BasicAlgo.format(
            prog_name=tmp_program_name,
            local_output_folder=docker_output_local_folder_BasicAlgo,
            local_program_path=tmp_program_path,
            testcases_folder=testcases_folder,
        )
        subprocess.run(docker_script, shell=True)

        # read the output and get the test-result
        test_output = load_file(output_file_path)
        result = test_output.startswith("True")
        failing_case = test_output[
            test_output.find("TEST CASE:") + len("TEST CASE:") : test_output.find("BUGGY OUTPUT:")
        ].strip()
        buggy_output = test_output[
            test_output.find("BUGGY OUTPUT:") + len("BUGGY OUTPUT:") : test_output.find("EXPECTED OUTPUT:")
        ].strip()
        expected_output = test_output[test_output.find("EXPECTED OUTPUT:") + len("EXPECTED OUTPUT:") :].strip()

        # remove the temporary files
        tmp_program_path.unlink()
        output_file_path.unlink()

        if result:  # return if True
            return result, "", "", ""

    return result, failing_case, buggy_output, expected_output
