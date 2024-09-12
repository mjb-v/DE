from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class PlanBase(BaseModel):
    year: int
    month: int
    item_id: int
    item_name: str
    category: str
    price: float
    standard: str
    module_name: str
    line: Optional[str] = None
    plan_quantity: int


class ProductionBase(BaseModel):
    date: date
    item_id: int
    item_name: str
    category: str
    price: float
    standard: str
    module_name: str
    line: Optional[str] = None
    worker_name: Optional[str] = None
    module_time: time
    working_time: time
    production_quantity: int
    bad_production: int
    bad_production_type: Optional[str] = None
    punching_quantity: int
    not_module_time: time


class InventoryManagementBase(BaseModel):
    date: date
    item_id: int
    item_name: str
    category: str
    price: float
    standard: str
    basic_quantity: int
    quantity_received: int
    defective_quantity_received: int
    quantity_shipped: int
    current_stock: int
    current_LOT_stock: int

class PlanResponse(BaseModel):
    total_plan_quantity: int
    total_business_plan: float
    total_production_quantity: int
    total_business_actual: float
    production_achievement_rate: float
    business_achievement_rate: float
    year: int
    month: int