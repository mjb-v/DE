# schemas.py
from pydantic import BaseModel

# 생산 데이터 생성용 스키마
class ProductionCreate(BaseModel):
    year: int
    line_name: str
    shift: str
    month: int
    production_quantity: float
    defect_quantity: float

# 연간 요약 데이터 생성용 스키마
class SummaryCreate(BaseModel):
    year: int
    line_name: str
    total_production: float
    total_defects: float

# 생산 데이터 응답 스키마
class Production(ProductionCreate):
    id: int

    class Config:
        orm_mode = True

# 연간 요약 데이터 응답 스키마
class Summary(SummaryCreate):
    id: int

    class Config:
        orm_mode = True
