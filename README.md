Data Migration from SQL DB to Redis <br />
<br />
Demo Steps: <br />
(1) Populate the SQLite DB by SQLalchemy <br />
(2) Migrate data from SQLite to Redis by redisco <br />
(3) Compare query execution time between SQL and Redis <br />
<br />
Demo Results: <br />
---------------------------------------------------------- <br />
SQL: Query user by name. <br />
Results: <model.sql_model.User object at 0x7fef63e75610> <br />
Execution time: 0.001375 <br />
<br />
---------------------------------------------------------- <br />
Redis: Query user by name. <br />
Results: [<User:500 {'created_at': datetime.datetime(2016, 4, 10, 17, 27, 46, 864874), 'last_name': u'jFSfofF', 'user_id': 500, 'first_name': u'pGq83dgot'}>] <br />
Execution time: 0.002313 <br />
<br />
---------------------------------------------------------- <br />
SQL: Query user created within a time interval. <br />
Results: 1000 <br />
Execution time: 0.017459 <br />
<br />
---------------------------------------------------------- <br />
Redis: Query user created within a time interval. <br />
Results: 1000 <br />
Execution time: 0.008786 <br />
<br />
---------------------------------------------------------- <br />
SQL: Query comments by user name. <br />
Results: 8 <br />
Execution time: 0.005967 <br />
<br />
---------------------------------------------------------- <br />
Redis: Query comments by user name. <br />
Results: 8 <br />
Execution time: 0.004468 <br />
