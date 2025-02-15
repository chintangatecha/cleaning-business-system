from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import sys

# Add the src directory to Python path
src_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if src_path not in sys.path:
    sys.path.append(src_path)

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cleaning_business.db")

# Handle special case for SQLite
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    # For PostgreSQL with SSL support
    engine = create_engine(
        DATABASE_URL,
        connect_args={
            "sslmode": "require"
        }
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    """Initialize the database tables"""
    Base.metadata.create_all(bind=engine)

# Initialize tables
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
