from typing import List, Any


def flatten(from_list: List[Any]) -> List[Any]:
    """ Flatten List[str] """
    flattened_list = []
    for item in from_list:
        if not isinstance(item, str):
            flattened_list.extend(flatten(item))
        else:
            flattened_list.append(item)
    return flattened_list
