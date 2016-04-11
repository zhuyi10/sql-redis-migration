"""

Redis-SQL Opertaions.

"""

import os
import sys

CUR_DIR = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(CUR_DIR, '..')))
import conn.sql_conn
import conn.redis_conn
from model import sql_model
from model import redis_model

def migrate_sql_to_redis(sql_db_url, redis_url):
    """ Migrate data from SQL to Redis. """
    print 'Migrating data from SQL to Redis'
    sql_session = conn.sql_conn.get_db_session(sql_db_url)
    conn.redis_conn.connection_setup(redis_url)
    for sql_user in sql_session.query(sql_model.User):
        redis_user = redis_model.User(user_id=sql_user.id,
                                      created_at=sql_user.created_at,
                                      first_name=sql_user.first_name,
                                      last_name=sql_user.last_name)
        redis_user.save()
        for sql_comment in sql_session.query(sql_model.Comment).\
                                       filter_by(user_id=sql_user.id):
            redis_comment = redis_model.Comment(comment_id=sql_comment.id,
                                                created_at=sql_comment.created_at,
                                                comment=sql_comment.comment,
                                                user=redis_user)
            redis_comment.save()
