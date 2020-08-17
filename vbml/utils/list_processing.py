from typing import Sequence


def flatten(from_list: list) -> list:
    flattened_list = []
    for item in from_list:
        if isinstance(item, Sequence) and not isinstance(item, str):
            flattened_list.extend(flatten(item))
        else:
            flattened_list.append(item)
    return flattened_list
