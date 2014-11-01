from django.contrib.auth.models import User
from django.db import models
import markdown

from core.settings import CHALLENGE_NAME_LENGTH, FLAG_LENGTH, TEAM_NAME_LENGTH


class Challenge(models.Model):
    """A challenge represents an individual problem to be solved."""

    CATEGORY_CHOICES = (
        ('be', 'Beer'),
        ('cr', 'Crypto'),
        ('ex', 'Exploitation'),
        ('fo', 'Forensics'),
        ('rn', 'Recon'),
        ('re', 'Reversing'),
        ('we', 'Web'),
        ('mi', 'Miscellaneous'),
    )

    name = models.CharField(max_length=CHALLENGE_NAME_LENGTH)
    points = models.IntegerField()
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    flag = models.CharField(max_length=FLAG_LENGTH)
    description_markdown = models.TextField()
    description_html = models.TextField()

    def save(self, *args, **kwargs):
        self.description_html = markdown.markdown(self.description_markdown)
        super(Challenge, self).save(*args, **kwargs)

    def __str__(self):
        return "{} {}: {}".format(
            self.get_category_display(), self.points, self.name)


class Team(models.Model):
    """A team is a collection of players."""
    name = models.CharField(max_length=TEAM_NAME_LENGTH)
    creator = models.ForeignKey("Player", related_name="created_teams")

    def __str__(self):
        return self.name


class Player(User):
    """A player is a user with a team."""
    team = models.ForeignKey("Team", blank=True, null=True)


class Solution(models.Model):
    """A solution is a player's """
    challenge = models.ForeignKey("Challenge")
    solved_at = models.DateTimeField(auto_now_add=True)
    solver = models.ForeignKey("Player")

    def __str__(self):
        return "{} by {}".format(self.challenge, self.solver)
