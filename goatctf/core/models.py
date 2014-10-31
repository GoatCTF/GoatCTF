from django.db import models
from core.settings import FLAG_LENGTH


class Challenge(models.Model):
    """A challenge represents an individual problem to be solved."""
    points = models.IntegerField()
    category = models.CharField(max_length=2)
    flag = models.CharField(max_length=FLAG_LENGTH)
    description_markdown = models.TextField()
    description_html = models.TextField()
