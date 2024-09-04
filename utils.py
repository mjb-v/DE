# utils.py
import pandas as pd
from sqlalchemy.orm import Session
from models import ProductionRecord, InventoryManagement
from io import BytesIO
import json

async def process_file(file, db: Session):
    # 파일 확장자에 따라 처리 방식 결정
    file_extension = file.filename.split('.')[-1].lower()

    if file_extension == 'xlsx':
        await process_excel(file, db)
    elif file_extension == 'csv':
        await process_csv(file, db)
    elif file_extension == 'json':
        await process_json(file, db)
    else:
        raise ValueError("Unsupported file format. Please upload an Excel, CSV, or JSON file.")

async def process_excel(file, db: Session):
    content = await file.read()
    excel_data = pd.read_excel(BytesIO(content), sheet_name=None)
    
    for sheet_name, df in excel_data.items():
        df_cleaned = df.dropna(how='all')
        
        for index, row in df_cleaned.iterrows():
            if pd.isna(row.get('라인')) or pd.isna(row.get('주/야간')):
                continue
            
            # 데이터를 적절히 변환
            file_path = f"files/{file.filename}"
            production_record = ProductionRecord(file_path=file_path)
            db.add(production_record)
    
    db.commit()

async def process_csv(file, db: Session):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    
    df_cleaned = df.dropna(how='all')
    
    for index, row in df_cleaned.iterrows():
        if pd.isna(row.get('라인')) or pd.isna(row.get('주/야간')):
            continue
        
        # 데이터를 적절히 변환
        file_path = f"files/{file.filename}"
        production_record = ProductionRecord(file_path=file_path)
        db.add(production_record)
    
    db.commit()

async def process_json(file, db: Session):
    content = await file.read()
    data = json.loads(content)
    
    for entry in data:
        if '라인' not in entry or '주/야간' not in entry:
            continue
        
        # 데이터를 적절히 변환
        file_path = f"files/{file.filename}"
        production_record = ProductionRecord(file_path=file_path)
        db.add(production_record)
    
    db.commit()
