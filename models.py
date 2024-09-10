from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time
from sqlalchemy.orm import relationship
from database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer)
    quantity_plan = Column(Integer)

    productions = relationship("Production", back_populates="plan")


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    worker_name = Column(String(255))

    productions = relationship("Production", back_populates="worker")


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String(255))
    line = Column(String(50))

    productions = relationship("Production", back_populates="module")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(255))
    category = Column(String(100))
    price = Column(Integer)
    standard = Column(String(100))

    productions = relationship("Production", back_populates="item")
    inventory_managements = relationship("InventoryManagement", back_populates="item")


class Production(Base):
    __tablename__ = "productions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    module_id = Column(Integer, ForeignKey('modules.id'), index=True)
    module_time = Column(Time)
    worker_id = Column(Integer, ForeignKey('workers.id'), index=True)
    working_time = Column(Time)
    item_id = Column(Integer, ForeignKey('items.id'), index=True)
    production_quantity = Column(Integer)  # Corrected typo here
    bad_production = Column(Integer)  # Corrected typo here
    bad_production_type = Column(String(100))
    punching_quantity = Column(Integer)
    plan_id = Column(Integer, ForeignKey('plans.id'), index=True)

    item = relationship("Item", back_populates="productions")
    module = relationship("Module", back_populates="productions")
    worker = relationship("Worker", back_populates="productions")
    plan = relationship("Plan", back_populates="productions")


class InventoryManagement(Base):
    __tablename__ = "inventory_managements"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    item_id = Column(Integer, ForeignKey('items.id'), index=True)
    basic_quantity = Column(Integer)
    quantity_received = Column(Integer)
    defective_quantity_received = Column(Integer)
    quantity_shipped = Column(Integer)
    current_stock = Column(Integer)
    current_LOT_stock = Column(Integer)

    item = relationship("Item", back_populates="inventory_managements")
