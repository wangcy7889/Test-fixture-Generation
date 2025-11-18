import numpy as np

def process_item(reward_fn, data_source, response_lst, reward_data):
    ground_truth = reward_data['ground_truth']
    score_lst = [reward_fn(data_source, r, ground_truth) for r in response_lst]
    return (data_source, np.mean(score_lst))