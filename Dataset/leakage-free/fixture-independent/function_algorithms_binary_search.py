from algorithms.search import binary_search


def find_target_index(sorted_list, target):
    
    index = binary_search(sorted_list, target)
    return index if index is not None else -1
