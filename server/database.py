from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# データベースとの接続情報を設定します
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@db:5432/pcb_inventory"

# SQL Alchemyのエンジンを作成します
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# セッションの作成情報を設定します
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルを作成するための基本クラスを作成します
Base = declarative_base()
