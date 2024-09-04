# crud.py
from sqlalchemy.orm import Session
import models, schemas

def create_production_plan(db: Session, data: schemas.ProductionPlanCreate):
    db_plan = models.ProductionPlan(
        year=data.year,
        month=data.month,
        injection_line=data.injection_line,
        item_name=data.item_name,
        item_number=data.item_number,
        production_quantity=data.production_quantity,
        business_plan=data.business_plan,
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def create_production_record(db: Session, file_path: str):
    db_record = models.ProductionRecord(file_path=file_path)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def create_inventory_management(db: Session, file_path: str):
    db_record = models.InventoryManagement(file_path=file_path)
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_production_plans(db: Session, year: int):
    return db.query(models.ProductionPlan).filter(models.ProductionPlan.year == year).all()

def calculate_achievement_rate(db: Session, year: int, month: int):
    # 주어진 연도와 월에 해당하는 생산 계획을 조회
    plans = db.query(models.ProductionPlan).filter(
        models.ProductionPlan.year == year,
        models.ProductionPlan.month == month
    ).all()

    # 총 계획 생산량 및 사업 계획 합산
    total_plan_production = sum(plan.production_quantity for plan in plans)
    total_plan_business = sum(plan.business_plan for plan in plans)

    # 실제 생산량 (예시로 90%를 사용, 실제 로직으로 교체 필요)
    total_actual_production = sum(plan.production_quantity * 0.9 for plan in plans)  # 예시: 실제 생산량은 계획의 90%
    total_actual_business = sum(plan.business_plan * 0.95 for plan in plans)  # 예시: 실제 사업 실적은 계획의 95%

    # 달성률 계산
    production_achievement_rate = (total_actual_production / total_plan_production) * 100 if total_plan_production else 0
    business_achievement_rate = (total_actual_business / total_plan_business) * 100 if total_plan_business else 0

    return {
        "production_achievement_rate": production_achievement_rate,
        "business_achievement_rate": business_achievement_rate
    }


def get_monthly_performance(db: Session, year: int, month: str):
    # 월별 특정 카테고리(유형) 기준의 실적을 조회
    performance = db.query(models.ProductionRecord).filter(
        models.ProductionRecord.year == year,
        models.ProductionRecord.month == month
    ).all()
    
    # 실적을 기반으로 데이터 가공 (예시)
    return {"monthly_performance": performance}

def get_inventory_management(db: Session, start_date: str, end_date: str):
    return db.query(models.InventoryManagement).filter(
        models.InventoryManagement.upload_date.between(start_date, end_date)
    ).all()

def update_production_plan(db: Session, plan_id: int, update_data: dict):
    db_plan = db.query(models.ProductionPlan).filter(models.ProductionPlan.id == plan_id).first()
    if db_plan:
        for key, value in update_data.items():
            setattr(db_plan, key, value)
        db.commit()
        db.refresh(db_plan)
    return db_plan

def delete_production_plan(db: Session, plan_id: int):
    db_plan = db.query(models.ProductionPlan).filter(models.ProductionPlan.id == plan_id).first()
    if db_plan:
        db.delete(db_plan)
        db.commit()
    return db_plan