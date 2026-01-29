from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# SQLite for now (dev-friendly)
DATABASE_URL = "sqlite:///./x_agent.db"

# Engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # required for SQLite + Flask
    future=True,
    echo=False,
)

# Session factory
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True,
    )
)

# Base class for models
Base = declarative_base()



