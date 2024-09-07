import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from . import models

SQLALCHEMY_DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # connect_args={"check_same_thread": False}
)
# Create all tables in the database, used for testing locally
if 'sqlite' in SQLALCHEMY_DATABASE_URL:
    models.Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
