from fuzzywuzzy import fuzz

def compare_strings(str1: str, str2: str, threshold: int = 80):

    similarity = fuzz.ratio(str1, str2)  
    return similarity >= threshold  
