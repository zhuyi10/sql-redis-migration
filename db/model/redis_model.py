"""

Redis Model.

"""

import datetime

from redisco import models


class User(models.Model):
    user_id = models.IntegerField(indexed=True)
    created_at = models.DateTimeField(auto_now_add=True, indexed=True)
    first_name = models.Attribute(required=True, indexed=True)
    last_name = models.Attribute(required=True, indexed=True)


class Comment(models.Model):
    comment_id = models.IntegerField(indexed=True)
    created_at = models.DateTimeField(auto_now_add=True, indexed=True)
    comment = models.Attribute(required=True, indexed=True)
    user = models.ReferenceField(User, indexed=True)
