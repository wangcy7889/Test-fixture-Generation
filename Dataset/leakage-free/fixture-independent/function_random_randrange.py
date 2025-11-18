import random


def generate_random_randrange(start, stop=None, step=1, custom_check=None):
    result = random.randrange(start, stop, step)
    if custom_check:
        custom_check(result)
    return result