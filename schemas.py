from pydantic import BaseModel
from typing import Optional
import datetime

# 생산 실적 생성 스키마
class ProductionCreate(BaseModel):
    date: datetime.date
    module_id: int
    module_time: datetime.time
    worker_id: int
    working_time: datetime.time
    item_id: int
    production_quantity: int
    bad_production: int
    bad_production_type: str
    punching_quantity: int
    plan_id: int

    class Config:
        orm_mode = True

class ProductionUpdate(BaseModel):
    date: Optional[datetime.date] = None  
    module_id: Optional[int] = None
    module_time: Optional[datetime.time] = None
    worker_id: Optional[int] = None
    working_time: Optional[datetime.time] = None
    item_id: Optional[int] = None
    production_quantity: Optional[int] = None
    bad_production: Optional[int] = None
    bad_production_type: Optional[str] = None
    punching_quantity: Optional[int] = None
    plan_id: Optional[int] = None

# 재고 관리 생성 스키마
class InventoryManagementCreate(BaseModel):
    date: datetime.date
    item_id: int
    basic_quantity: int
    quantity_received: int
    defective_quantity_received: int
    quantity_shipped: int
    current_stock: int
    current_LOT_stock: int
    
    class Config:
        orm_mode = True

class InventoryManagementUpdate(BaseModel):
    date: Optional[datetime.date] = None 
    item_id: Optional[int] = None
    basic_quantity: Optional[int] = None
    quantity_received: Optional[int] = None
    defective_quantity_received: Optional[int] = None
    quantity_shipped: Optional[int] = None
    current_stock: Optional[int] = None
    current_LOT_stock: Optional[int] = None