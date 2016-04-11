"""

SQL DB operations.

"""

import os
import sys
import random

CUR_DIR = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(CUR_DIR, '..')))
from conn.sql_conn import get_db_engine, get_db_session
from model import sql_model

CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


def _generate_rand_str(length_range_start, length_range_end):
    """ Generate a random string.
        The range of it's length is (length_range_start, length_range_end).
    """
    length = random.randint(length_range_start, length_range_end)
    return ''.join([random.choice(CHARS) for i in range(length)])


def create_db_schema(db_url):
    """ Create DB schema. """
    print 'Creating DB schema.'
    sql_model.Base.metadata.create_all(get_db_engine(db_url))


def populate_db(db_url, num_users, range_comments):
    """ Populate DB.
        num_users -- total number of users.
        range_comments -- range total number of comments per user (start, end).
    """
    print 'Populating DB.'
    session = get_db_session(db_url)
    for i in xrange(num_users):
        session.add(sql_model.User(first_name=_generate_rand_str(5, 10),
                                   last_name=_generate_rand_str(5, 10)))
        for j in xrange(range_comments[0], range_comments[1]):
            session.add(sql_model.Comment(comment=_generate_rand_str(10, 50),
                                          user_id=i))
    session.commit()
    session.close()


def get_user_by_id(session, user_id):
    """ Get user by id. """
    return session.query(sql_model.User).filter_by(id=user_id).one()


def get_user_by_name(session, first_name, last_name):
    """ Get user by first name and last name. """
    return session.query(sql_model.User).filter_by(
                   first_name=first_name, last_name=last_name).one()


def get_users_by_time_range(session, time_start_at, time_end_at):
    """ Get all users created within the time interval. """
    return session.query(sql_model.User).filter(
                   sql_model.User.created_at > time_start_at,
                   sql_model.User.created_at < time_end_at).all()


def get_comments_by_user_name(session, first_name, last_name):
    """ Get comments by user's first name and last name. """
    user = get_user_by_name(session, first_name, last_name)
    comments = session.query(sql_model.Comment).join(sql_model.User).filter(
                       sql_model.Comment.user_id == user.id).all()
    return comments
