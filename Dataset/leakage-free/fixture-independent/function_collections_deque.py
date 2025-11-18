from collections import deque


def deque_operations_helper(operation_type):
    d = deque()
    if operation_type == 'append_and_appendleft':
        d.append(1)
        d.appendleft(0)
        return list(d)
    elif operation_type == 'extend_and_extendleft':
        d.extend([2, 3])
        d.extendleft([1, 0])
        return list(d)
    elif operation_type == 'pop_and_popleft':
        d = deque([1, 2, 3])
        d.popleft()
        d.pop()
        return len(d)
    elif operation_type == 'rotate':
        d = deque([1, 2, 3])
        d.rotate(1)
        rotated_result = list(d)
        d.rotate(-2)
        return rotated_result, list(d)
    elif operation_type == 'count':
        d = deque([1, 2, 2, 3])
        return d.count(2)
    elif operation_type =='remove':
        d = deque([1, 2, 3])
        d.remove(2)
        return list(d)
    elif operation_type == 'clear':
        d = deque([1, 2, 3])
        d.clear()
        return len(d)