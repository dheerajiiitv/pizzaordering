import json
import uuid
from random import random
from typing import List, Union

from fastapi import FastAPI, Depends

from models import PizzaMenu, PizzaOrderRequest, PizzaOrderResponse
from exceptions import PizzaIDNotPresent
app = FastAPI()


def get_pizza_data() -> List[PizzaMenu]:
    data = json.load(open("mock_data.json", "r"))
    return [PizzaMenu.parse_obj(i) for i in data]

@app.get("/")
def pizza_world():
    return"Welcome"
@app.get("/menu", response_model=Union[PizzaMenu, str])
def get_pizza_details(query: str, pizzas_data: List[PizzaMenu] = Depends(get_pizza_data)):

    for pizza_detail in pizzas_data:
        if pizza_detail.name == query:
            return pizza_detail

    return "No Pizza found"


@app.post("/order", response_model=PizzaOrderResponse)
def order_pizza(request: List[PizzaOrderRequest], pizzas_data: List[PizzaMenu] = Depends(get_pizza_data)):
    order_id = 1234
    total_price = 0

    for pizza_request in request:
        # Get price
        present=False
        for pizza_detail in pizzas_data:
            if pizza_request.id == pizza_detail.id:
                present=True
                total_price += pizza_detail.price * pizza_request.quantity

        if not present:
            raise PizzaIDNotPresent(detail="Pizza ID not present", status_code=404)
    return PizzaOrderResponse(order_id=order_id, price=total_price)
