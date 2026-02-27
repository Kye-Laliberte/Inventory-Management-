from pydantic import BaseModel, validator, Field,  constr
from typing import Optional
from enum import Enum



        
class statusTable(str,Enum):
    active = "active"
    inactive = "inactive"

class ItemCreate(BaseModel):
    name: str
    category: str
    price: float = Field(gt=0)
    tags: Optional[str] = None
    status: Optional[str] = "active"
    description: Optional[str] = None
    @validator("status")
    def validat_status(cls, v):
        if v not in ("inactive", "active"):
            raise ValueError("Invalid status")
        



class Store(BaseModel):
    store_id: int
    name: str
    location: str
    status: str
    store_code: str

class StoreCreate(BaseModel):
    name: str
    location: str
    status: Optional[str] = "active"
    @validator("status")
    def validate_status(cls, v):
        if v not in ("active", "inactive"):
            raise ValueError("Invalid status")
        return v
    
    