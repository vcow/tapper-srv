from django.contrib.auth.models import User
from django.db import models


class Record(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    scores = models.BigIntegerField(default=0, db_index=True)
    data = models.TextField(null=True)
