from bashplotlib.histogram import plot_hist as bashplotlib_plot_hist
from datetime import datetime


def plot_histogram(data):
    if not isinstance(data, list):
        raise TypeError("Error: Data must be provided as a list.")
    if not data:
        raise ValueError("Error: Data list cannot be empty.")

    current_time = datetime.now()
    if current_time.hour < 8 or current_time.hour > 22:
        raise ValueError("Error: Histogram plotting is only available between 08:00-22:00 UTC")

    bashplotlib_plot_hist(data)
    return True
