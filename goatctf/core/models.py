from django.contrib.auth.models import User
from django.db import models
from core.settings import TEAM_NAME_LENGTH, FLAG_LENGTH


class Challenge(models.Model):
    """A challenge represents an individual problem to be solved."""
    points = models.IntegerField()
    category = models.CharField(max_length=2)
    flag = models.CharField(max_length=FLAG_LENGTH)
    description_markdown = models.TextField()
    description_html = models.TextField()


class Team(models.Model):
    """A team is a collection of players."""
    name = models.CharField(max_length=TEAM_NAME_LENGTH)
    creator = models.ForeignKey("Player", related_name="created_teams")


class Player(User):
    """A player is a user with a team."""
    team = models.ForeignKey("Team")
