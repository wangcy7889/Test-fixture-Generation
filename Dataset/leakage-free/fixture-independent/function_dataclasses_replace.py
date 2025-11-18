from dataclasses import dataclass, replace

@dataclass
class Car:
    brand: str
    model: str
    year: int

def update_dataclass_field(instance, **kwargs):
    
    try:
        if not hasattr(instance, "__dataclass_fields__"):
            raise ValueError("The input object is not a dataclass instance.")
        return replace(instance, **kwargs)
    except Exception as e:
        raise ValueError(f"Error in updating dataclass field: {e}")
