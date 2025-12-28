from __future__ import annotations
import gguf
def get_field(reader, field_name, field_type):
    field = reader.get_field(field_name)
    if field is None:
        return None
    elif isinstance(field_type, str):
        if len(field.types) != 1 or field.types[0] != gguf.GGUFValueType.STRING:
            raise TypeError(f"Bad type for GGUF {field_name} key: expected string, got {field.types!r}")
        return str(field.parts[field.data[-1]], encoding="utf-8")
    elif field_type in [int, float, bool]:
        return field_type(field.parts[field.data[-1]])
    else:
        raise TypeError(f"Unknown field type {field_type}")
