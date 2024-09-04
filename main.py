# main.py
from fastapi import FastAPI, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db
from utils import process_file

# 모델을 기반으로 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI()

# CREATE
# 생산 계획 엔드포인트
@app.post("/production_plan/", response_model=schemas.ProductionPlan)
def create_production_plan(data: schemas.ProductionPlanCreate, db: Session = Depends(get_db)):
    return crud.create_production_plan(db, data)

# 생산 실적 엔드포인트
@app.post("/production_record/")
async def upload_production_record(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        # 데이터베이스에 기록
        db_record = crud.create_production_record(db, file_location)
        return {"message": "Production record uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 재고관리 엔드포인트
@app.post("/inventory_management/")
async def upload_inventory_management(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        file_location = f"files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(file.file.read())
        
        # 데이터베이스에 기록
        db_record = crud.create_inventory_management(db, file_location)
        return {"message": "Inventory management record uploaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#READ
# 연도생산계획 조회
@app.get("/production_plan/{year}", response_model=list[schemas.ProductionPlan])
def read_production_plan(year: int, db: Session = Depends(get_db)):
    plans = crud.get_production_plans(db, year)
    if not plans:
        raise HTTPException(status_code=404, detail="Production plans not found")
    return plans

# 월별달성률 조회
@app.get("/achievement_rate/{year}/{month}", response_model=dict)
def read_achievement_rate(year: int, month: int, db: Session = Depends(get_db)):
    achievement_rate = crud.calculate_achievement_rate(db, year, month)
    if not achievement_rate:
        raise HTTPException(status_code=404, detail="Achievement rate not found")
    return achievement_rate

# 월 실적 조회
@app.get("/monthly_performance/{year}/{category}", response_model=dict)
def read_monthly_performance(year: int, category: str, db: Session = Depends(get_db)):
    performance = crud.get_monthly_performance(db, year, category)
    if not performance:
        raise HTTPException(status_code=404, detail="Monthly performance not found")
    return performance

# 재고관리 조회
@app.get("/inventory_management/", response_model=list[schemas.InventoryManagement])
def read_inventory_management(start_date: str, end_date: str, db: Session = Depends(get_db)):
    inventories = crud.get_inventory_management(db, start_date, end_date)
    if not inventories:
        raise HTTPException(status_code=404, detail="Inventory records not found")
    return inventories

@app.put("/production_plan/{plan_id}", response_model=schemas.ProductionPlan)
def update_production_plan(plan_id: int, data: dict, db: Session = Depends(get_db)):
    updated_plan = crud.update_production_plan(db, plan_id, data)
    if updated_plan is None:
        raise HTTPException(status_code=404, detail="Production plan not found")
    return updated_plan

@app.delete("/production_plan/{plan_id}", response_model=schemas.ProductionPlan)
def delete_production_plan(plan_id: int, db: Session = Depends(get_db)):
    deleted_plan = crud.delete_production_plan(db, plan_id)
    if deleted_plan is None:
        raise HTTPException(status_code=404, detail="Production plan not found")
    return deleted_plan