from pydantic import BaseModel, PositiveFloat, ValidationError
from typing import Annotated

StockType = Annotated[int, 0 <= 1000]  

class Product(BaseModel):
    stock: Annotated[int, 0 <= 1000]
    price: PositiveFloat 

def create_product(stock: int, price: float):
    try:
        product = Product(stock=stock, price=price)
        return product
    except ValidationError as e:
        return e.errors()  

