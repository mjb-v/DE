# models.py
from sqlalchemy import Column, Integer, String, Float
from database import Base

# LineProduction 모델
class LineProduction(Base):
    __tablename__ = "line_production"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    line_name = Column(String, index=True)
    shift = Column(String)
    month = Column(Integer)
    production_quantity = Column(Float)
    defect_quantity = Column(Float)

# AnnualSummary 모델
class AnnualSummary(Base):
    __tablename__ = "annual_summary"
    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, index=True)
    line_name = Column(String, index=True)
    total_production = Column(Float)
    total_defects = Column(Float)
