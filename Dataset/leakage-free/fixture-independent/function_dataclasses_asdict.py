from dataclasses import dataclass, asdict, field
from typing import List

@dataclass
class Person:
    name: str
    age: int
    hobbies: List[str] = field(default_factory=list)

def dataclass_to_dict(obj):
    
    try:
        if not hasattr(obj, "__dataclass_fields__"):
            raise ValueError("The input object is not a dataclass instance.")
        return asdict(obj)
    except Exception as e:
        raise ValueError(f"Error in converting dataclass to dict: {e}")
