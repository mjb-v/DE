
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas, datetime
from database import get_db



app = FastAPI()

# 의존성 주입을 위한 데이터베이스 세션

# CREATE: 생산 실적 생성
@app.post("/productions/", response_model=schemas.ProductionCreate)
def create_production(production: schemas.ProductionCreate, db: Session = Depends(get_db)):
    return crud.create_production(db=db, production_data=production)

@app.get("/productions/{production_id}", response_model=schemas.ProductionCreate)
def read_production(production_id: int, db: Session = Depends(get_db)):
    db_production = crud.get_production(db, production_id=production_id)
    if db_production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return db_production

@app.get("/productions/date/{query_date}", response_model=list[schemas.ProductionCreate])
def read_productions_by_date(query_date: datetime.date, db: Session = Depends(get_db)):
    productions = crud.get_productions_by_date(db, query_date)
    if not productions:
        raise HTTPException(status_code=404, detail="No productions found for this date")
    return productions

@app.put("/productions/{production_id}", response_model=schemas.ProductionUpdate)
def update_production(production_id: int, production_update: schemas.ProductionUpdate, db: Session = Depends(get_db)):
    # 생산 기록을 조회
    production = db.query(models.Production).filter(models.Production.id == production_id).first()
    
    if not production:
        raise HTTPException(status_code=404, detail="Production record not found")
    
    # 필드 업데이트
    for key, value in production_update.dict().items():
        setattr(production, key, value)
    
    db.commit()
    db.refresh(production)
    
    return production

@app.delete("/productions/{production_id}")
def delete_production(production_id: int, db: Session = Depends(get_db)):
    # 생산 기록을 조회
    production = db.query(models.Production).filter(models.Production.id == production_id).first()
    
    if not production:
        raise HTTPException(status_code=404, detail="Production record not found")
    
    db.delete(production)
    db.commit()
    
    return {"detail": "Production record deleted successfully"}

# CREATE: 재고 관리 생성
@app.post("/inventory_management/", response_model=schemas.InventoryManagementCreate)
def create_inventory_management(inventory: schemas.InventoryManagementCreate, db: Session = Depends(get_db)):
    return crud.create_inventory_management(db=db, inventory=inventory)

@app.get("/inventory_management/{inventory_id}", response_model=schemas.InventoryManagementCreate)
def read_inventory_management(inventory_id: int, db: Session = Depends(get_db)):
    db_inventory = crud.get_inventory_management(db, inventory_id=inventory_id)
    if db_inventory is None:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    return db_inventory

@app.get("/inventory_management/date/{query_date}", response_model=list[schemas.InventoryManagementCreate])
def read_inventory_by_date(query_date: datetime.date, db: Session = Depends(get_db)):
    inventories = crud.get_inventory_by_date(db, query_date)
    if not inventories:
        raise HTTPException(status_code=404, detail="No inventory records found for this date")
    return inventories

@app.put("/inventory/{inventory_id}", response_model=schemas.InventoryManagementUpdate)
def update_inventory(inventory_id: int, inventory_update: schemas.InventoryManagementUpdate, db: Session = Depends(get_db)):
    # 재고 기록을 조회
    inventory = db.query(models.InventoryManagement).filter(models.InventoryManagement.id == inventory_id).first()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    # 필드 업데이트
    for key, value in inventory_update.dict().items():
        setattr(inventory, key, value)
    
    db.commit()
    db.refresh(inventory)
    
    return inventory

@app.delete("/inventory/{inventory_id}")
def delete_inventory(inventory_id: int, db: Session = Depends(get_db)):
    # 재고 기록을 조회
    inventory = db.query(models.InventoryManagement).filter(models.InventoryManagement.id == inventory_id).first()
    
    if not inventory:
        raise HTTPException(status_code=404, detail="Inventory record not found")
    
    db.delete(inventory)
    db.commit()
    
    return {"detail": "Inventory record deleted successfully"}
