import re
from typing import Optional


def strip_line(line: str) -> str:
    """Remove trailing spaces and tabs"""
    line = re.sub(r"[\t ]+$", "", line)
    return line


def strip_program(program: Optional[str]) -> Optional[str]:
    """Remove redundant spaces and empty-lines such as leading empty-lines and trailing spaces/empty-lines"""
    if program is None:
        return None

    # remove trailing empty line at the beginning of the program
    program = program.lstrip("\n")
    # remove trailing spaces at the end of the program
    program = re.sub(r"[\r\n\t ]+$", "", program)
    # remove trailing spaces at the end of each line
    lines = program.split("\n")
    lines = [strip_line(line) for line in lines]
    program = "\n".join(lines)
    # append an end-line at the end of the program
    program += "\n"

    return program
