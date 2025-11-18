from dataclasses import fields

def get_dataclass_fields(dataclass_instance):
    
    try:
        if not hasattr(dataclass_instance, "__dataclass_fields__"):
            raise ValueError("Error: The input object is not a dataclass instance.")
        return [(field.name, field.type) for field in fields(dataclass_instance)]
    except Exception as e:
        raise ValueError(f"Error in retrieving dataclass fields: {e}")
