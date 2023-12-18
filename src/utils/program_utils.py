import re
import sys
from pathlib import Path
from typing import List, Union

import pygments
from pygments.lexers.python import PythonLexer

sys.path.append(".")


def load_program(program_path: Union[Path, str]):
    """Load and return a program"""

    with open(program_path, "r") as f:
        program = f.read()
    return program


lexer = PythonLexer()


def lex_program(program: str):
    """Use pygments.lexers.python.PythonLexer to lex the given program"""
    return list(lexer.get_tokens(program))


def program_to_essential_tokens(program: str, strip_chars="\n\r\t\f ") -> List[str]:
    """
    Simplify the program by removing unnecessary tokens, including:
        - comments
        - all spaces after the first non-space token in each line
        - blank lines with/without spaces
        - trailing spaces at the end of the program
    """
    simplified_program_tokens = []

    if isinstance(program, float) or program is None or len(program) == 0:
        return [""]

    lines = program.split("\n")
    meaningful_lines = [line for line in lines if line.strip(strip_chars) != ""]
    program_without_blank_lines = "\n".join(meaningful_lines)

    lex_output = lex_program(program_without_blank_lines)
    is_start_of_line = True
    for component in lex_output:
        token_type, token_value = component
        if token_type == pygments.token.Whitespace and token_value == "\n":
            is_start_of_line = True
            if len(simplified_program_tokens) == 0 or simplified_program_tokens[-1] != "\n":
                simplified_program_tokens.append(token_value)
        elif not is_start_of_line and token_type == pygments.token.Text and re.match(r"^\s+$", token_value):
            pass  # drop all unnecessary spaces (i.e. all space tokens after the first non-space token in every line)
        elif token_type in pygments.token.Comment.subtypes:
            pass  # drop all comments
        else:
            simplified_program_tokens.append(token_value)
            is_start_of_line = False

    while len(simplified_program_tokens) > 0 and simplified_program_tokens[-1].strip(strip_chars) == "":
        del simplified_program_tokens[-1]

    return simplified_program_tokens
