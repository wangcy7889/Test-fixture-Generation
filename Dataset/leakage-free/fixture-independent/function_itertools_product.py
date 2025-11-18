import itertools



def f_product(lists):
    return [list(row) for row in itertools.product(*lists)]

