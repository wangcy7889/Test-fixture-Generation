from pydantic import BaseModel, ValidationError

class User(BaseModel):
    name: str
    age: int
    email: str

def create_user(name: str, age: int, email: str):
    try:
        user = User(name=name, age=age, email=email)
        return user
    except ValidationError as e:
        return e.errors()  
