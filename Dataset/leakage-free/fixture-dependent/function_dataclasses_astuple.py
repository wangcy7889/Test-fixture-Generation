from dataclasses import astuple

def convert_dataclass_to_tuple(dataclass_instance):

    try:
        if not hasattr(dataclass_instance, "__dataclass_fields__"):
            raise ValueError("Error: The input object is not a dataclass instance.")
        return astuple(dataclass_instance)
    except Exception as e:
        raise ValueError(f"Error converting dataclass to tuple: {e}")
