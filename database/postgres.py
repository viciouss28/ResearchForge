
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from .env")


engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    echo=False,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

Base = declarative_base()


def get_db():
    """Provide a database session."""

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def test_postgres():

    with engine.connect() as connection:

        result = connection.execute(
            text("SELECT version();")
        )

        print("[POSTGRES] Connected successfully!")
        print(result.scalar())

