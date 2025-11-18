import time
from tenacity import retry, stop_after_attempt, wait_fixed


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def might_fail_function(value, extra_sleep=0):
    print(f"The current value is: {value}")
    time.sleep(extra_sleep)
    if value < 5:
        raise ValueError("Value is too small")
    return value

