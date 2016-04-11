"""

Redis DB operations.

"""

import os
import sys
import random

CUR_DIR = os.path.dirname(__file__)
sys.path.append(os.path.realpath(os.path.join(CUR_DIR, '..')))
from model import redis_model


def get_user_by_name(first_name, last_name):
    """ Get user by first name and last name. """
    return redis_model.User.objects.filter(first_name=first_name,
                                           last_name=last_name)


def get_users_by_time_range(time_start_at, time_end_at):
    """ Get all users created within the time interval. """
    return redis_model.User.objects.zfilter(
                            created_at__in=(time_start_at,
                                            time_end_at))


def get_comments_by_user_name(first_name, last_name):
    """ Get comments by user's first name and last name. """
    user = redis_model.User.objects.filter(first_name=first_name,
                                           last_name=last_name)
    return redis_model.Comment.objects.filter(user_id=user.first().user_id)
