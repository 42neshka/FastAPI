from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQL_DB_URL = 'sqlite:///./alexnode3.db'

engine = create_engine(SQL_DB_URL, connect_args={'check_same_thread': False})

session_local = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()