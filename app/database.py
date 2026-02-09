from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase,Session


DATABASE_URL="sqlite:///./notes.db"

engine=create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread":False}
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SessionLocal=sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

