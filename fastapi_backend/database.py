from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

user = "postgres"
password = "ycdc2021"
host = "192.168.16.28"
db = "postgres"
port='5432'

SQLALCHEMY_DATABASE_URL=f"postgresql://{user}:{password}@{host}:{port}/{db}"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

#SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
db_session = scoped_session(sessionmaker(bind=engine, autocommit=False, autoflush=False))

Base = declarative_base()
Base.query = db_session.query_property()

def get_db():
    db = db_session()
    try:
        yield db
    finally:
        db.close()