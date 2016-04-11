#!/usr/bin/env python
"""

Demo

Data Migration from SQL DB to Redis.
Export data from SQL DB by SQLalchemy.
http://www.sqlalchemy.org/
Import data into Redis by Redisco.
https://github.com/kiddouk/redisco

"""

import datetime
import os
import subprocess
import sys
import time

import db.conn.sql_conn
import db.conn.redis_conn
import db.operations.ops
import db.operations.sql_ops
import db.operations.redis_ops

CUR_DIR = os.path.dirname(__file__)
TEST_DB_PATH = os.path.join(os.path.realpath(CUR_DIR), 'test.db')
SQL_DB_URL = 'sqlite:///' + TEST_DB_PATH
REDIS_URL = 'redis://127.0.0.1:6379/0'
NUM_USERS = 5000
RANGE_COMMENTS = (2, 10)


def create_sql_test_db():
    """ Create a test DB and populate random data. """
    if os.path.isfile(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    try:
        subprocess.check_call('sqlite3 ' + TEST_DB_PATH + ' \'\'', shell=True)
        db.operations.sql_ops.create_db_schema(SQL_DB_URL)
        db.operations.sql_ops.populate_db(db_url=SQL_DB_URL,
                                          num_users=NUM_USERS,
                                          range_comments=RANGE_COMMENTS)
    except subprocess.CalledProcessError:
        raise Exception('Failed to create the test DB.')


def main():
    create_sql_test_db()
    db.operations.ops.migrate_sql_to_redis(sql_db_url=SQL_DB_URL,
                                           redis_url=REDIS_URL)

    # Compare query execution time
    # Use user 500 as an example
    db.conn.redis_conn.connection_setup(REDIS_URL)
    sql_session = db.conn.sql_conn.get_db_session(SQL_DB_URL)
    user = db.operations.sql_ops.get_user_by_id(sql_session, 500)

    print '\n----------------------------------------------------------'
    print 'SQL: Query user by name.'
    start_time = time.time()
    rs_user = db.operations.sql_ops.get_user_by_name(sql_session,
                                                     user.first_name,
                                                     user.last_name)
    print 'Results: ' + str(rs_user)
    print 'Execution time: %f' % (time.time() - start_time)

    print '\n----------------------------------------------------------'
    print 'Redis: Query user by name.'
    start_time = time.time()
    rs_user = db.operations.redis_ops.get_user_by_name(user.first_name,
                                                       user.last_name)
    print 'Results: ' + str(rs_user)
    print 'Execution time: %f' % (time.time() - start_time)

    print '\n----------------------------------------------------------'
    print 'SQL: Query user created within a time interval.'
    start_time = time.time()
    rs_user = db.operations.sql_ops.get_users_by_time_range(
                 sql_session,
                 datetime.datetime.now() - datetime.timedelta(seconds=10),
                 datetime.datetime.now())
    print 'Results: %d' % len(rs_user)
    print 'Execution time: %f' % (time.time() - start_time)

    print '\n----------------------------------------------------------'
    print 'Redis: Query user created within a time interval.'
    start_time = time.time()
    rs_user = db.operations.redis_ops.get_users_by_time_range(
                 datetime.datetime.now() - datetime.timedelta(seconds=10),
                 datetime.datetime.now())
    print 'Results: %d' % len(rs_user)
    print 'Execution time: %f' % (time.time() - start_time)

    print '\n----------------------------------------------------------'
    print 'SQL: Query comments by user name. '
    start_time = time.time()
    rs_comments = db.operations.sql_ops.get_comments_by_user_name(
                     sql_session, user.first_name, user.last_name)
    print 'Results: %d' % len(rs_comments)
    print 'Execution time: %f' % (time.time() - start_time)

    print '\n----------------------------------------------------------'
    print 'Redis: Query comments by user name. '
    start_time = time.time()
    rs_comments = db.operations.redis_ops.get_comments_by_user_name(
                     user.first_name, user.last_name)
    print 'Results: %d' % len(rs_comments)
    print 'Execution time: %f' % (time.time() - start_time)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
