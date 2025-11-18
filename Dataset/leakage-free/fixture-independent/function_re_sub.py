import re

def f_sub(text, target_word, replacement_word,num):
    return re.sub(target_word, replacement_word, text,num)