
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:1234@localhost:5432/taskflow_db"
)
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal=sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()  
          
