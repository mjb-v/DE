# crud.py
from sqlalchemy.orm import Session
from models import LineProduction, AnnualSummary
from schemas import ProductionCreate, SummaryCreate

# 새로운 생산 데이터 생성
def create_production(db: Session, production: ProductionCreate):
    db_production = LineProduction(
        year=production.year,
        line_name=production.line_name,
        shift=production.shift,
        month=production.month,
        production_quantity=production.production_quantity,
        defect_quantity=production.defect_quantity
    )
    db.add(db_production)
    db.commit()
    db.refresh(db_production)
    return db_production

# 새로운 연간 요약 데이터 생성
def create_summary(db: Session, summary: SummaryCreate):
    db_summary = AnnualSummary(
        year=summary.year,
        line_name=summary.line_name,
        total_production=summary.total_production,
        total_defects=summary.total_defects
    )
    db.add(db_summary)
    db.commit()
    db.refresh(db_summary)
    return db_summary

# 특정 라인의 생산 데이터 조회
def get_production(db: Session, year: int, line_name: str):
    return db.query(LineProduction).filter(LineProduction.year == year, LineProduction.line_name == line_name).all()

# 특정 라인의 연간 요약 데이터 조회
def get_summary(db: Session, year: int, line_name: str):
    return db.query(AnnualSummary).filter(AnnualSummary.year == year, AnnualSummary.line_name == line_name).first()
