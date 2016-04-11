"""

SQL DB Connection.

"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def get_db_engine(db_url):
    """ Get the instance of DB engine.
        postgresql+psycopg2://username:password@host/dbname
        db_url example: postgresql+psycopg2://readonly:readonly@127.0.0.1/testdb
    """
    return create_engine(db_url)


def get_db_session(db_url):
    """ Get DB sesssion. """
    return sessionmaker(bind=get_db_engine(db_url))()
