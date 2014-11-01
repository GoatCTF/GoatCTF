from django.db.utils import IntegrityError
import pytest

from core.models import Player, Team


@pytest.fixture
def user():
    user = Player()
    user.username = 'user'
    user.password = ''
    user.save()
    return user


@pytest.mark.django_db
def test_cannot_create_without_creator(user):
    team1 = Team(name="Team 1")
    with pytest.raises(IntegrityError):
        team1.save()


@pytest.mark.django_db
def test_team_names_are_unique(user):
    team1 = Team(name="Team 1", creator=user)
    team1.save()

    team2 = Team(name="Team 1", creator=user)
    with pytest.raises(IntegrityError):
        team2.save()
