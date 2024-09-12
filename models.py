from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, Float
from database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    month = Column(Integer)
    item_id = Column(Integer)
    item_name = Column(String(100))
    category = Column(String(100))
    price = Column(Float)
    standard = Column(String(100))
    module_name = Column(String(100))
    line = Column(String)
    plan_quantity = Column(Integer)
    


class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    item_id = Column(Integer)
    item_name = Column(String(100))
    category = Column(String(100))
    price = Column(Float)
    standard = Column(String(100))
    module_name = Column(String(100))
    line = Column(String)
    worker_name = Column(String(100))
    module_time = Column(Time)
    working_time = Column(Time)
    production_quantity = Column(Integer)  # Corrected typo here
    bad_production = Column(Integer)  # Corrected typo here
    bad_production_type = Column(String(100))
    punching_quantity = Column(Integer)
    not_module_time = Column(Time)

class InventoryManagement(Base):
    __tablename__ = "inventory_managements"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    item_id = Column(Integer)
    item_name = Column(String(100))
    category = Column(String(100))
    price = Column(Float)
    standard = Column(String(100))
    basic_quantity = Column(Integer)
    quantity_received = Column(Integer)
    defective_quantity_received = Column(Integer)
    quantity_shipped = Column(Integer)
    current_stock = Column(Integer)
    current_LOT_stock = Column(Integer)

