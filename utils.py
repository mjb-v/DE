# utils.py
import pandas as pd
from sqlalchemy.orm import Session
from models import LineProduction
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
            
            for month_idx, month in enumerate(["01월", "02월", "03월", "04월", "05월", "06월", 
                                               "07월", "08월", "09월", "10월", "11월", "12월"], start=1):
                production = row.get(month)
                defect_col = f"Unnamed: {df.columns.get_loc(month)+1}"
                defect = row.get(defect_col)
                
                if pd.notna(production) and pd.notna(defect):
                    production_record = LineProduction(
                        year=int(file.filename.split('_')[3]),
                        line_name=row['라인'],
                        shift=row['주/야간'],
                        month=month_idx,
                        production_quantity=production,
                        defect_quantity=defect
                    )
                    db.add(production_record)
    db.commit()

async def process_csv(file, db: Session):
    content = await file.read()
    df = pd.read_csv(BytesIO(content))
    
    df_cleaned = df.dropna(how='all')
    
    for index, row in df_cleaned.iterrows():
        if pd.isna(row.get('라인')) or pd.isna(row.get('주/야간')):
            continue
        
        for month_idx, month in enumerate(["01월", "02월", "03월", "04월", "05월", "06월", 
                                           "07월", "08월", "09월", "10월", "11월", "12월"], start=1):
            production = row.get(month)
            defect_col = f"Unnamed: {df.columns.get_loc(month)+1}"
            defect = row.get(defect_col)
            
            if pd.notna(production) and pd.notna(defect):
                production_record = LineProduction(
                    year=int(file.filename.split('_')[3]),
                    line_name=row['라인'],
                    shift=row['주/야간'],
                    month=month_idx,
                    production_quantity=production,
                    defect_quantity=defect
                )
                db.add(production_record)
    db.commit()

async def process_json(file, db: Session):
    content = await file.read()
    data = json.loads(content)
    
    for entry in data:
        if '라인' not in entry or '주/야간' not in entry:
            continue
        
        year = int(file.filename.split('_')[3])
        line_name = entry['라인']
        shift = entry['주/야간']
        
        for month_idx, month in enumerate(["01월", "02월", "03월", "04월", "05월", "06월", 
                                           "07월", "08월", "09월", "10월", "11월", "12월"], start=1):
            production_key = f"{month}_생산량"
            defect_key = f"{month}_불량량"
            
            production = entry.get(production_key)
            defect = entry.get(defect_key)
            
            if production is not None and defect is not None:
                production_record = LineProduction(
                    year=year,
                    line_name=line_name,
                    shift=shift,
                    month=month_idx,
                    production_quantity=production,
                    defect_quantity=defect
                )
                db.add(production_record)
    db.commit()
