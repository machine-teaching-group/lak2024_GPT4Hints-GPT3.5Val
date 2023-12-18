import argparse
import json
import os  # noqa: F401
import subprocess
import time
from pathlib import Path


def read_file(path: Path):
    with open(path, "r") as f:
        content = f.read()
        return content


def write_file(path: Path, content: str):
    with open(path, "w") as f:
        f.write(content)


def save_tmp_file(content: str, extension: str = ".py") -> Path:
    """Write `content` to a tmp file and return the path to that file"""
    tmp_folder = Path("tmp_folder")
    tmp_folder.mkdir(exist_ok=True)
    tmp_file = tmp_folder / f"{str(time.time())}{extension}"
    write_file(path=tmp_file, content=content)
    return tmp_file


def read_json(path: Path):
    with open(path, "r") as f:
        content = json.load(f)
        return content


def main(args):
    program_path = Path(args.program_path)
    tests_path = Path(args.tests_path)

    program_id = program_path.stem

    test_program = read_file(program_path) + "\n\n" + read_file(tests_path)
    test_program_path = save_tmp_file(content=test_program)

    # Run the tests and get result
    try:
        run_result = subprocess.run(["python", test_program_path], capture_output=True, timeout=10)
        verdict = run_result.stdout.endswith(b"NO ASSERTION CAUGHT!\n")
        if verdict:
            output = ""
        else:
            if run_result.stdout.strip():
                output = run_result.stdout.decode().strip()
            else:
                output = run_result.stderr.decode().strip().split("\n")[-1]
    except subprocess.TimeoutExpired:
        verdict = False
        output = "Time Limit Exceeded"

    # write_file(path=Path("output") / f"{program_id}.py", content=str(verdict))
    write_file(path=Path("output") / f"{program_id}.py", content=f"{verdict}\n\nBUGGY OUTPUT:{output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program_path", type=Path, help="Path to the program file.")
    parser.add_argument("tests_path", type=Path, help="Path to the test file.")

    args = parser.parse_args()
    main(args)
