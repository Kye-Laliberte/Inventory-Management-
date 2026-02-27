
from pydantic import BaseModel, validator, Field,  constr
from typing import Optional
from enum import Enum

class createInventory(BaseModel):
    item_id: int
    store_id: str
    quantity: Optional[int] =0
    status: str

class Inventory(BaseModel):
    item_id: int
    item_name: str
    quantity: int
    price: float
    category_name: str
    status: str

class InventoryItem(BaseModel):
    item_id: int
    item_name: str
    quantity: int
    price: float
    category_name: str