from schematics.types import BaseType
from schematics.exceptions import ValidationError

class IntegerListType(BaseType):

    def to_primitive(self, value):
        
        if not isinstance(value, list):
            raise ValidationError("Value must be a list.")
        
        if not all(isinstance(item, int) for item in value):
            raise ValidationError("All items in the list must be integers.")
        
        return value
