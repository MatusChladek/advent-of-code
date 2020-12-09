from typing import List


def get_data(file_relative_path: str) -> List[str]:
    with open(file_relative_path) as f:
        data = [line.rstrip() for line in f]
        return data
