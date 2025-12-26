from dataclasses import dataclass
from typing import List

@dataclass
class OrderItem:
    product_category: str
    quantity: int
    price: float

@dataclass
class OrderEvent:
    order_id: str
    timestamp: str
    customer_state: str
    items: List[OrderItem]
    payment_value: float

