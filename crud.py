from sqlalchemy.orm import Session
import models, schemas, datetime


# CREATE: 생산 실적 생성
def create_production(db: Session, production_data: schemas.ProductionCreate):
    db_production = models.Production(
        date=production_data.date,
        module_id=production_data.module_id,
        module_time=production_data.module_time,
        worker_id=production_data.worker_id,
        working_time=production_data.working_time,
        item_id=production_data.item_id,
        production_quantity=production_data.production_quantity,
        bad_production=production_data.bad_production,
        bad_production_type=production_data.bad_production_type,
        punching_quantity=production_data.punching_quantity,
        plan_id=production_data.plan_id
    )
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

def get_production(db: Session, production_id: int):
    return db.query(models.Production).filter(models.Production.id == production_id).first()

def get_productions_by_date(db: Session, query_date: datetime.date):
    return db.query(models.Production).filter(models.Production.date == query_date).all()

# CREATE: 재고 관리 생성
def create_inventory_management(db: Session, inventory: schemas.InventoryManagementCreate):
    db_inventory = models.InventoryManagement(
        date=inventory.date,
        item_id=inventory.item_id,
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

# READ: 월별 재고 관리 조회
def get_inventory_management(db: Session, inventory_id: int):
    return db.query(models.InventoryManagement).filter(models.InventoryManagement.id == inventory_id).first()

def get_inventory_by_date(db: Session, query_date: datetime.date):
    return db.query(models.InventoryManagement).filter(models.InventoryManagement.date == query_date).all()