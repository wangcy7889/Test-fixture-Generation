import sys


def process_arguments():
    if len(sys.argv) > 1:
        print(f"Received arguments: {sys.argv[1:]}")
        return sys.argv[1:]
    print("No arguments provided.")
    return []