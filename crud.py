from sqlalchemy.orm import Session
from models import Plan, Production, InventoryManagement
import schemas
from sqlalchemy import func
from typing import List

# Plan CRUD
def create_plan(db: Session, plan: schemas.PlanBase):
    db_plan = Plan(
        year=plan.year,
        month=plan.month,
        item_id=plan.item_id,
        item_name=plan.item_name,
        category=plan.category,
        price=plan.price,
        standard=plan.standard,
        module_name=plan.module_name,
        line=plan.line,
        plan_quantity=plan.plan_quantity
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_all_plans(db: Session, year: int, month: int) -> schemas.PlanResponse:
    total_plan_quantity = db.query(Plan).filter(Plan.year == year, Plan.month == month).with_entities(func.sum(Plan.plan_quantity)).scalar() or 0
    total_business_plan = db.query(Plan).filter(Plan.year == year, Plan.month == month).with_entities(func.sum(Plan.plan_quantity * Plan.price)).scalar() or 0

    total_production_quantity = db.query(Production).filter(Production.date.between(f'{year}-{month:02d}-01', f'{year}-{month:02d}-31')).with_entities(func.sum(Production.production_quantity)).scalar() or 0

    total_business_actual = db.query(Production).filter(Production.date.between(f'{year}-{month:02d}-01', f'{year}-{month:02d}-31')).with_entities(func.sum(Production.production_quantity * Production.price)).scalar() or 0

    production_achievement_rate = (total_production_quantity / total_plan_quantity) * 100 if total_plan_quantity > 0 else 0
    business_achievement_rate = (total_business_actual / total_business_plan) * 100 if total_business_plan > 0 else 0

    return schemas.PlanResponse(
        total_plan_quantity=total_plan_quantity,
        total_business_plan=total_business_plan,
        total_production_quantity=total_production_quantity,
        total_business_actual=total_business_actual,
        production_achievement_rate=production_achievement_rate,
        business_achievement_rate=business_achievement_rate,
        year=year,
        month=month
    )

# Production CRUD
def create_production(db: Session, production: schemas.ProductionBase):
    db_production = Production(
        date=production.date,
        item_id=production.item_id,
        item_name=production.item_name,
        category=production.category,
        price=production.price,
        standard=production.standard,
        module_name=production.module_name,
        line=production.line,
        worker_name=production.worker_name,
        module_time=production.module_time,
        working_time=production.working_time,
        production_quantity=production.production_quantity,
        bad_production=production.bad_production,
        bad_production_type=production.bad_production_type,
        punching_quantity=production.punching_quantity,
        not_module_time=production.not_module_time
    )
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

def get_production(db: Session, production_id: int):
    return db.query(Production).filter(Production.id == production_id).first()

def get_all_productions(db: Session):
    return db.query(Production).all()

# InventoryManagement CRUD
def create_inventory_management(db: Session, inventory: schemas.InventoryManagementBase):
    db_inventory = InventoryManagement(
        date=inventory.date,
        item_id=inventory.item_id,
        item_name=inventory.item_name,
        category=inventory.category,
        price=inventory.price,
        standard=inventory.standard,
        basic_quantity=inventory.basic_quantity,
        quantity_received=inventory.quantity_received,
        defective_quantity_received=inventory.defective_quantity_received,
        quantity_shipped=inventory.quantity_shipped,
        current_stock=inventory.current_stock,
        current_LOT_stock=inventory.current_LOT_stock
    )
    db.add(db_inventory)
    db.commit()
    db.refresh(db_inventory)
    return db_inventory

def get_inventory(db: Session, inventory_id: int):
    return db.query(InventoryManagement).filter(InventoryManagement.id == inventory_id).first()

def get_all_inventories(db: Session):
    return db.query(InventoryManagement).all()