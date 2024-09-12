
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import crud, models, schemas, datetime
from database import get_db
from typing import List

app = FastAPI()

@app.post("/plans/", response_model=schemas.PlanBase)
def create_plan(plan: schemas.PlanBase, db: Session = Depends(get_db)):
    return crud.create_plan(db=db, plan=plan)

@app.get("/plans/", response_model=schemas.PlanResponse)
def get_plans(year: int, month: int, db: Session = Depends(get_db)):
    return crud.get_all_plans(db=db, year=year, month=month)

# Production Endpoints
@app.post("/productions/", response_model=schemas.ProductionBase)
def create_production(production: schemas.ProductionBase, db: Session = Depends(get_db)):
    return crud.create_production(db=db, production=production)

@app.get("/productions/{production_id}", response_model=schemas.ProductionBase)
def get_production(production_id: int, db: Session = Depends(get_db)):
    production = crud.get_production(db=db, production_id=production_id)
    if production is None:
        raise HTTPException(status_code=404, detail="Production not found")
    return production

@app.get("/productions/", response_model=List[schemas.ProductionBase])
def get_all_productions(db: Session = Depends(get_db)):
    return crud.get_all_productions(db=db)

# Inventory Management Endpoints
@app.post("/inventories/", response_model=schemas.InventoryManagementBase)
def create_inventory_management(inventory: schemas.InventoryManagementBase, db: Session = Depends(get_db)):
    return crud.create_inventory_management(db=db, inventory=inventory)

@app.get("/inventories/{inventory_id}", response_model=schemas.InventoryManagementBase)
def get_inventory(inventory_id: int, db: Session = Depends(get_db)):
    inventory = crud.get_inventory(db=db, inventory_id=inventory_id)
    if inventory is None:
        raise HTTPException(status_code=404, detail="Inventory not found")
    return inventory

@app.get("/inventories/", response_model=List[schemas.InventoryManagementBase])
def get_all_inventories(db: Session = Depends(get_db)):
    return crud.get_all_inventories(db=db)