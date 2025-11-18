import re
from fuzzywuzzy import process

def find_best_match(query: str, choices: list, threshold: int = 80):
    
    query_clean = re.sub(r'\W+', '', query)
    choices_clean = [re.sub(r'\W+', '', choice) for choice in choices]
    
    best_match = process.extractOne(query_clean, choices_clean)
    if best_match and best_match[1] >= threshold:
        return (choices[choices_clean.index(best_match[0])], best_match[1])
    return None