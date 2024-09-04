# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date
from sqlalchemy.orm import relationship
from database import Base

#생산계획
class ProductionPlan(Base):
    __tablename__ = "production_plans"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    month = Column(Integer, index=True)
    injection_line = Column(String, index=True)
    item_name = Column(String, index=True)
    item_number = Column(String, index=True)
    production_quantity = Column(Integer)
    business_plan = Column(Float)

#생산실적
class ProductionRecord(Base):
    __tablename__ = "production_records"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)

#재고관리
class InventoryManagement(Base):
    __tablename__ = "inventory_management"

    id = Column(Integer, primary_key=True, index=True)
    file_path = Column(String)
    upload_date = Column(Date, index=True)