from .config import Settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

print(Settings.DATABASE_URL)  # before create_engine

engine = create_engine(
    Settings.DATABASE_URL,
    echo=Settings.DEBUG,
    pool_pre_ping=True,
    connect_args={"sslmode": "require"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
