# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import engine, get_db

# 모델을 기반으로 데이터베이스 테이블 생성
models.Base.metadata.create_all(bind=engine)

# FastAPI 앱 생성
app = FastAPI()

# 생산 데이터 생성 엔드포인트
@app.post("/production/", response_model=schemas.Production)
def create_production(data: schemas.ProductionCreate, db: Session = Depends(get_db)):
    return crud.create_production(db, data)

# 연간 요약 데이터 생성 엔드포인트
@app.post("/summary/", response_model=schemas.Summary)
def create_summary(data: schemas.SummaryCreate, db: Session = Depends(get_db)):
    return crud.create_summary(db, data)

# 특정 라인의 생산 데이터 조회 엔드포인트
@app.get("/production/{year}/{line_name}", response_model=list[schemas.Production])
def read_production(year: int, line_name: str, db: Session = Depends(get_db)):
    data = crud.get_production(db, year, line_name)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

# 특정 라인의 연간 요약 데이터 조회 엔드포인트
@app.get("/summary/{year}/{line_name}", response_model=schemas.Summary)
def read_summary(year: int, line_name: str, db: Session = Depends(get_db)):
    summary = crud.get_summary(db, year, line_name)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary
