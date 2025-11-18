import numpy as np

def calculate_turn_around_time(process_name: list, arrival_time: list, burst_time: list, no_of_process: int) -> list:
    current_time = 0
    finished_process_count = 0
    finished_process = [0] * no_of_process
    turn_around_time = [0] * no_of_process
    burst_time = [burst_time[i] for i in np.argsort(arrival_time)]
    process_name = [process_name[i] for i in np.argsort(arrival_time)]
    arrival_time.sort()
    while no_of_process > finished_process_count:
        i = 0
        while finished_process[i] == 1:
            i += 1
        current_time = max(current_time, arrival_time[i])
        response_ratio = 0
        loc = 0
        temp = 0
        for i in range(no_of_process):
            if finished_process[i] == 0 and arrival_time[i] <= current_time:
                temp = (burst_time[i] + (current_time - arrival_time[i])) / burst_time[i]
            if response_ratio < temp:
                response_ratio = temp
                loc = i
        turn_around_time[loc] = current_time + burst_time[loc] - arrival_time[loc]
        current_time += burst_time[loc]
        finished_process[loc] = 1
        finished_process_count += 1
    return turn_around_time