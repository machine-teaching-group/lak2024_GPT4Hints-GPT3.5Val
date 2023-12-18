import sys
from pathlib import Path

sys.path.append(".")

from src.utils.IO_utils import load_json_file


def load_source_data(
    source_data_path: Path,
):
    """
    Load the source data file.
    Return: data in JSON format
    """

    # Load file
    data_json = load_json_file(source_data_path)

    # sort by program name
    data_json = sorted(data_json, key=lambda x: x["program"]["name"])

    return data_json
