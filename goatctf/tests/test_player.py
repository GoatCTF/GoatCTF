from django.db.utils import IntegrityError
import pytest

from core.models import Player, Team


@pytest.fixture
def player_factory():
    class PlayerFactory(object):
        def get(self):
            user = Player()
            i=0
            while Player.objects.filter(username=str(i)).count() > 0:
                i+=1
            user.username = str(i)
            user.password = ''
            user.save()
            return user
    return PlayerFactory()


@pytest.mark.django_db
def test_creator_team_equal(player_factory):
    player1 = player_factory.get()
    team1 = Team(name="Team 1", creator=player1)
    team1.save()

    player2 = player_factory.get()
    team2 = Team(name="Team 2", creator=player2)
    team2.save()

    player1.team = team2
    with pytest.raises(IntegrityError):
        player1.save()
