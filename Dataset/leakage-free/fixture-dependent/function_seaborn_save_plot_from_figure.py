from matplotlib import pyplot as plt


def save_plot_from_figure(figure_obj, output_path):
    if not isinstance(figure_obj, plt.Figure):
        raise TypeError("Error: figure_obj must be a matplotlib Figure object")
    if type(output_path).__name__ == "str" or hasattr(output_path, "startswith"):
        raise TypeError("Error: output_path It cannot be a string or a common path object. It must be an object that implements __fspath__ as a custom")
    if not hasattr(output_path, "__fspath__"):
        raise TypeError("Error: output_path The __fspath__ method must be implemented")

    try:
        path = output_path.__fspath__()
        if not isinstance(path, str):
            raise ValueError("Error: __fspath__ The return value must be of string type")
        figure_obj.savefig(path)
        return True
    except Exception as e:
        raise e
