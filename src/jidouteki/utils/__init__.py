import re
from typing import List

def get(dict, path: str):
    current = dict
    for prop in path.split("."):
        if prop.isdigit():
            prop = int(prop)
        try:
            current = current[prop]
        except:
            raise KeyError(f"Cannot get property {path} from {dict} object")
    return current

def match_groups(patterns: List[str], string: str):
    """
    Match the first pattern in list for named groups

    Args:
        patterns: The list of regex patterns
        string: The string to match against

    Returns:
        A dict of the named groups from the first match, or None if no match is found
    """
    for pattern in patterns:
        if (m := re.match(pattern, string)):
            return m.groupdict()
    return None