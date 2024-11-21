from enum import Enum

from pydantic import BaseModel
from typing import List


class PizzaSize(str, Enum):
    SMALL = "Small"
    MEDIUM = "Medium"
    LARGE = "Large"


class PizzaMenu(BaseModel):
    id: int
    name: str
    price: float
    size: PizzaSize
    toppings: List[str]

class PizzaOrderRequest(BaseModel):
    id: int
    quantity: int

class PizzaOrderResponse(BaseModel):
    order_id: int
    price: float