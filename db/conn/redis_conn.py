"""

Redis Connection.

"""

import re

import redisco


def connection_setup(db_url):
    """ Setup DB connnection.
        redis://host:port/testdb
        db_url example: redis://127.0.0.1:6379/0
    """
    match = re.search(r'redis://(?P<host>.*):(?P<port>\d*)/(?P<dbname>.*)', db_url)
    redisco.connection_setup(host=match.group('host'),
                             port=match.group('port'),
                             db=match.group('dbname'))
