import argparse
import json
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
    tests_path = Path("testcases/")

    program_id = program_path.stem

    # Check the number of testcases
    test_files = list(tests_path.glob("*.txt"))
    assert len(test_files) % 2 == 0, f"There are {len(test_files)} test files, which is invalid"
    n_cases = len(test_files) // 2
    for i in range(1, n_cases + 1):
        assert (
            tests_path / f"{i}_inp.txt"
        ).is_file(), f"`{i}_inp.txt` does not exist while there are {n_cases} test cases"
        assert (
            tests_path / f"{i}_out.txt"
        ).is_file(), f"`{i}_out.txt` does not exist while there are {n_cases} test cases"

    # Run the tests and get result
    for i in range(1, n_cases + 1):
        inp = read_file(tests_path / f"{i}_inp.txt").strip()
        expected_out = read_file(tests_path / f"{i}_out.txt").strip()
        try:
            run_result = subprocess.run(
                ["python", program_path], input=inp, capture_output=True, encoding="utf8", timeout=2
            )
            out = run_result.stdout.strip()
            if out == "":
                out = run_result.stderr.strip().split("\n")[-1]
            if out != expected_out:
                verdict = "False"
                output = out
                break
        except subprocess.TimeoutExpired:
            verdict = "False"
            output = "Time Limit Exceeded"
            break
    else:
        verdict = "True"
        output = ""
        expected_out = ""
        inp = ""

    # write_file(path=Path("output") / f"{program_id}.py", content=verdict)
    write_file(
        path=Path("output") / f"{program_id}.py",
        content=f"{verdict}\n\nTEST CASE:{inp}\n\nBUGGY OUTPUT:{output}\n\nEXPECTED OUTPUT:{expected_out}",
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("program_path", type=Path, help="Path to the program file.")
    # assume test cases are placed in folder `testcases/`

    args = parser.parse_args()
    main(args)
