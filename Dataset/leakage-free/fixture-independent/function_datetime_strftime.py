from datetime import datetime

def format_current_time(input_time=None):
    if input_time is None:
        input_time = datetime.now()
    formatted_time = input_time.strftime("%Y-%m-%d %H:%M:%S")
    return formatted_time

# 不再包含 main 代码块
