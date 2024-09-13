import random
import time as t
from datetime import datetime, timedelta, time
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Production, InventoryManagement
from schemas import ProductionBase, InventoryManagementBase
from database import SessionLocal

def generate_random_production_data():
    return ProductionBase(
        date=(datetime.now() - timedelta(days=random.randint(0, 30))).date(),
        item_id=random.randint(1, 100),
        item_name=f"Item{random.randint(1, 100)}",
        category=f"Category{random.randint(1, 10)}",
        price=round(random.uniform(10.0, 500.0), 2),
        standard=f"Standard{random.randint(1, 5)}",
        module_name=f"Module{random.randint(1, 10)}",
        line=f"Line{random.randint(1, 5)}",
        worker_name=f"Worker{random.randint(1, 50)}",
        module_time=time(hour=random.randint(0, 23), minute=random.randint(0, 59)),
        working_time=time(hour=random.randint(0, 23), minute=random.randint(0, 59)),
        production_quantity=random.randint(1, 100),
        bad_production=random.randint(0, 10),
        bad_production_type=f"Type{random.randint(1, 5)}",
        punching_quantity=random.randint(0, 20),
        not_module_time=time(hour=random.randint(0, 23), minute=random.randint(0, 59))
    )

def insert_production_data(db: Session, production_data: ProductionBase):
    db_production = Production(
        date=production_data.date,
        item_id=production_data.item_id,
        item_name=production_data.item_name,
        category=production_data.category,
        price=production_data.price,
        standard=production_data.standard,
        module_name=production_data.module_name,
        line=production_data.line,
        worker_name=production_data.worker_name,
        module_time=production_data.module_time,
        working_time=production_data.working_time,
        production_quantity=production_data.production_quantity,
        bad_production=production_data.bad_production,
        bad_production_type=production_data.bad_production_type,
        punching_quantity=production_data.punching_quantity,
        not_module_time=production_data.not_module_time
    )
    db.add(db_production)
    db.commit()

def generate_random_inventory_data():
    return InventoryManagementBase(
        date=(datetime.now() - timedelta(days=random.randint(0, 30))).date(),
        item_id=random.randint(1, 100),
        item_name=f"Item{random.randint(1, 100)}",
        category=f"Category{random.randint(1, 10)}",
        price=round(random.uniform(10.0, 500.0), 2),
        standard=f"Standard{random.randint(1, 5)}",
        basic_quantity=random.randint(1, 100),
        quantity_received=random.randint(0, 100),
        defective_quantity_received=random.randint(0, 20),
        quantity_shipped=random.randint(0, 100),
        current_stock=random.randint(0, 200),
        current_LOT_stock=random.randint(0, 200)
    )

def insert_inventory_data(db: Session, Invetory_data: InventoryManagementBase):
    db_inventory = InventoryManagement(
        date=Invetory_data.date,
        item_id=Invetory_data.item_id,
        item_name=Invetory_data.item_name,
        category=Invetory_data.category,
        price=Invetory_data.price,
        standard=Invetory_data.standard,
        basic_quantity=Invetory_data.basic_quantity,
        quantity_received=Invetory_data.quantity_received,
        defective_quantity_received=Invetory_data.defective_quantity_received,
        quantity_shipped=Invetory_data.quantity_shipped,
        current_stock=Invetory_data.current_stock,
        current_LOT_stock=Invetory_data.current_LOT_stock
    )
    db.add(db_inventory)
    db.commit()

def main():
    db = SessionLocal()
    try:
        while True:
            production_data = generate_random_production_data()
            Invetory_data = generate_random_inventory_data()
            insert_production_data(db, production_data)
            insert_inventory_data(db, Invetory_data)
            print(f"Inserted: {production_data}, {Invetory_data}")
            t.sleep(10)  # 10초 대기
    finally:
        db.close()

if __name__ == "__main__":
    main()