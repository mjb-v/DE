# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
# SQLite 데이터베이스 URL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 베이스 클래스 생성
Base = declarative_base()

# Dependency: 요청마다 데이터베이스 세션을 생성하고 종료하는 역할
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
