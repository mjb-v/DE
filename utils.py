import pandas as pd
from sqlalchemy.orm import Session
from models import ProductionRecord
from io import BytesIO
import json
import re

async def process_file(file, db: Session):
    # 파일 확장자에 따라 처리 방식 결정
    file_extension = file.filename.split('.')[-1].lower()

    # 파일 이름에서 연도 추출 (예: "production_2024.xlsx"에서 2024 추출)
    year = extract_year_from_filename(file.filename)

    if file_extension == 'xlsx':
        await process_excel(file, db, year)
    elif file_extension == 'csv':
        await process_csv(file, db, year)
    elif file_extension == 'json':
        await process_json(file, db, year)
    else:
        raise ValueError("Unsupported file format. Please upload an Excel, CSV, or JSON file.")

def extract_year_from_filename(filename: str) -> int:
    match = re.search(r'\b(19|20)\d{2}\b', filename)  # 1900-2099년 사이의 연도 추출
    if match:
        return int(match.group(0))
    else:
        raise ValueError("Filename does not contain a valid year")

async def process_excel(file, db: Session, year: int):
    content = await file.read()
    excel_data = pd.read_excel(BytesIO(content), sheet_name=None)
    
    for sheet_name, df in excel_data.items():
        df_cleaned = df.dropna(how='all')
        
        for index, row in df_cleaned.iterrows():
            if pd.isna(row.get('라인')) or pd.isna(row.get('월')) or pd.isna(row.get('생산수량')):
                continue
            
            # 데이터를 적절히 변환하여 DB에 저장
            production_record = ProductionRecord(
                year=year,
                line=row['라인'],
                month=int(row['월']),
                production_quantity=int(row['생산수량'])
            )
            db.add(production_record)
    
    db.commit()

async def process_csv(file, db: Session, year: int):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    
    df_cleaned = df.dropna(how='all')
    
    for index, row in df_cleaned.iterrows():
        if pd.isna(row.get('라인')) or pd.isna(row.get('월')) or pd.isna(row.get('생산수량')):
            continue
        
        # 데이터를 적절히 변환하여 DB에 저장
        production_record = ProductionRecord(
            year=year,
            line=row['라인'],
            month=int(row['월']),
            production_quantity=int(row['생산수량'])
        )
        db.add(production_record)
    
    db.commit()

async def process_json(file, db: Session, year: int):
    content = await file.read()
    data = json.loads(content)
    
    for entry in data:
        if '라인' not in entry or '월' not in entry or '생산수량' not in entry:
            continue
        
        # 데이터를 적절히 변환하여 DB에 저장
        production_record = ProductionRecord(
            year=year,
            line=entry['라인'],
            month=int(entry['월']),
            production_quantity=int(entry['생산수량'])
        )
        db.add(production_record)
    
    db.commit()
