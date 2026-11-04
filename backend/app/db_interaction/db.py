from sqlalchemy import create_engine #type: ignore
from sqlalchemy.orm import sessionmaker, DeclarativeBase #type: ignore

from backend.app.config import DATABASE_URL

engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
