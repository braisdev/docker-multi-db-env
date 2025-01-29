import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

MYSQL_USER = os.getenv("MYSQL_USER", "testuser")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "testpass")
MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")  # Changed from 'mysql' to '127.0.0.1'
MYSQL_PORT = os.getenv("MYSQL_PORT", "3306")
MYSQL_DB = os.getenv("MYSQL_DATABASE", "mydb")

DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData()
metadata.reflect(bind=engine)


def get_mysql_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
