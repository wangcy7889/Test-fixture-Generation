import re


def text_match(pattern, text):
    match_result = re.match(pattern, text)
    if match_result:
        return match_result.group()
    return None