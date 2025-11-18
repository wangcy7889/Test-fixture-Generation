from collections import defaultdict


def count_words(word_list):
    word_count = defaultdict(int)
    for word in word_list:
        if isinstance(word, str):
            processed_word = word.lower().strip()
            if processed_word:
                word_count[processed_word] += 1
    return dict(word_count)
