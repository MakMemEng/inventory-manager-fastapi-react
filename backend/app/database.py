from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import config

# SQL Alchemyのエンジンを作成します
engine = create_engine(config.DATABASE_URL)

# セッションの作成情報を設定します
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルを作成するための基本クラスを作成します
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
