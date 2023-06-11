from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy.engine import URL


url = URL.create(
    drivername="postgresql",
    port="5432",
    username="Postgres",
    password="Postgres"
)

engine = create_engine("postgresql+psycopg2://postgres:psql@127.0.0.1:5432/users")

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close_all()