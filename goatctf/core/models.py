from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError
import markdown

from core.settings import CHALLENGE_NAME_LENGTH, FLAG_LENGTH, TEAM_NAME_LENGTH
from django_gravatar.helpers import get_gravatar_url, has_gravatar

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
    name = models.CharField(max_length=TEAM_NAME_LENGTH, unique=True)
    creator = models.ForeignKey("Player", related_name="created_teams")

    @classmethod
    def get_leaderboard(self):
        sum_points = models.Sum('player__solution__challenge__points')
        max_solved_at = models.Max('player__solution__solved_at')
        all_annotated = Team.objects.all().annotate(points=sum_points)
        all_annotated = all_annotated.annotate(solved_at=max_solved_at)
        all_sorted = all_annotated.order_by('-points', 'solved_at')
        return all_sorted

    def save(self, *args, **kwargs):
        if not hasattr(self, 'creator'):
            raise IntegrityError("Creator must be defined.")
        if self.creator.team and self.creator.team != self:
            raise IntegrityError("Creator must be a part of the team")
        super(Team, self).save(*args, **kwargs)
        self.creator.team = self
        self.creator.save()

    def __str__(self):
        return self.name


class Player(User):
    """A player is a user with a team."""
    team = models.ForeignKey("Team", blank=True, null=True)

    def save(self, *args, **kwargs):
        teams_exist = self.team and self.created_teams.count() > 0 
        if teams_exist and self.team != self.created_teams.all()[0]:
            raise IntegrityError("Player must be a part of all created teams!")
        super(Player, self).save(*args, **kwargs)

    def get_gravatar_url(self, size=150):
        return get_gravatar_url(self.email, size)

    def has_gravatar(self):
        return has_gravatar(self.email)

class Solution(models.Model):
    """A solution is a record of a player's successful attempt of a challenge."""
    challenge = models.ForeignKey("Challenge")
    solved_at = models.DateTimeField(auto_now_add=True)
    solver = models.ForeignKey("Player")

    def __str__(self):
        return "{} by {}".format(self.challenge, self.solver)


class JoinRequest(models.Model):
    """A join request is a request from a (non-creator) user to join a Team."""
    player = models.OneToOneField("Player")
    team = models.ForeignKey("Team")

    def approve(self):
        self.player.team = self.team
        self.player.save()
        self.delete()

    def cancel(self):
        self.delete()

