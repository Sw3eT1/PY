from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
import os

if os.getenv("DATABASE_URL"):
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data.db')}"

connect_args = {}
if "sqlite" in SQLALCHEMY_DATABASE_URL:
    connect_args = {"check_same_thread": False}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args=connect_args
)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))