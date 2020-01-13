from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker
from src.conf.pg_conf import postgres_db


def connect_pg():
    DATABASE_URL = str(URL(**postgres_db))
    pg_connection_engine = create_engine(DATABASE_URL, pool_size=1, max_overflow=20,
                                         connect_args={'connect_timeout': 10})
    return pg_connection_engine


def session_maker():
    pg_connection = connect_pg()
    Session = sessionmaker()
    Session.configure(bind=pg_connection)
    session = Session()
    return session
