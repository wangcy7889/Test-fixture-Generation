from fuzzywuzzy import fuzz

def compare_partial_strings(str1: str, str2: str, threshold: int = 80):

    similarity = fuzz.partial_ratio(str1, str2) 
    return similarity >= threshold  