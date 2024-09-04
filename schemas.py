# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductionPlanBase(BaseModel):
    year: int
    month: int
    injection_line: str
    item_name: str
    item_number: str
    production_quantity: int
    business_plan: float

class ProductionPlanCreate(ProductionPlanBase):
    pass

class ProductionPlan(ProductionPlanBase):
    id: int

    class Config:
        orm_mode: True

class ProductionRecordBase(BaseModel):
    file_path: str

class ProductionRecordCreate(ProductionRecordBase):
    pass

class ProductionRecord(ProductionRecordBase):
    id: int

    class Config:
        orm_mode: True

class InventoryManagementBase(BaseModel):
    file_path: str
    upload_date: date

class InventoryManagementCreate(InventoryManagementBase):
    pass

class InventoryManagement(InventoryManagementBase):
    id: int

    class Config:
        orm_mode: True
