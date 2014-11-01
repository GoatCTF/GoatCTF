from django.db.utils import IntegrityError
import pytest

from core.models import Player, Team, JoinRequest


@pytest.fixture
def player_factory():
    class PlayerFactory(object):
        def get(self):
            user = Player()
            # FIXME There must be a cleaner way to do this.
            i = 0
            while Player.objects.filter(username=str(i)).count() > 0:
                i += 1
            user.username = str(i)
            user.password = ''
            user.save()
            return user
    return PlayerFactory()


@pytest.mark.django_db
def test_cannot_create_without_creator():
    team1 = Team(name="Team 1")
    with pytest.raises(IntegrityError):
        team1.save()


@pytest.mark.django_db
def test_team_names_are_unique(player_factory):
    user1 = player_factory.get()
    team1 = Team(name="Team 1", creator=user1)
    team1.save()

    user2 = player_factory.get()
    team2 = Team(name="Team 1", creator=user2)
    with pytest.raises(IntegrityError):
        team2.save()


@pytest.mark.django_db
def test_creators_are_unique(player_factory):
    user = player_factory.get()

    team1 = Team(name="Team 1", creator=user)
    team1.save()

    team2 = Team(name="Team 2", creator=user)
    with pytest.raises(IntegrityError):
        team2.save()

@pytest.mark.django_db
def test_join_request_approve(player_factory):
    user1 = player_factory.get()
    user2 = player_factory.get()

    team = Team(name="Team", creator=user1)
    team.save()

    request = JoinRequest(player=user2, team=team)
    request.save()

    assert user2.team is None
    assert request.pk is not None
    request.approve()
    assert request.pk is None
    assert user2.team == team


@pytest.mark.django_db
def test_join_request_cancel(player_factory):
    user1 = player_factory.get()
    user2 = player_factory.get()

    team = Team(name="Team", creator=user1)
    team.save()

    request = JoinRequest(player=user2, team=team)
    request.save()

    assert user2.team is None
    assert request.pk is not None
    request.cancel()
    assert user2.team is None
    assert request.pk is None
 
