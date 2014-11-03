from django.db.utils import IntegrityError
import pytest

from core.models import Challenge, Player, Team, Solution, JoinRequest


@pytest.fixture
def challenge():
    challenge = Challenge()
    challenge.name = "Test Challenge"
    challenge.points = 100
    challenge.category = 'mi'
    challenge.flag = "test"
    challenge.description_markdown = """# Title
## Subtitle

Paragraph

Another paragraph
"""
    challenge.save()
    return challenge


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


@pytest.fixture
def fresh_team(player_factory):
    Team.objects.all().delete()
    team = Team(name="Team", creator=player_factory.get())
    team.save()
    return team


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
def test_leaderboard_empty_with_no_teams(challenge):
    assert len(Team.get_leaderboard()) == 0


@pytest.mark.django_db
def test_leaderboard_not_empty_with_one_team(challenge, fresh_team):
    leaderboard = Team.get_leaderboard()
    assert (leaderboard[0] == fresh_team and
            len(leaderboard) == 1)


@pytest.mark.django_db
def test_leaderboard_sorts_by_points(challenge, player_factory, fresh_team):
    other_team = Team(name="Team with Score", creator=player_factory.get())
    other_team.save()
    member = Player(username='player', password='', team=other_team)
    member.save()
    Solution(challenge=challenge, solver=member).save()
    leaderboard = Team.get_leaderboard()
    assert (leaderboard[0] == other_team and
            leaderboard[1] == fresh_team and
            len(leaderboard) == 2)


@pytest.mark.django_db
def test_leaderboard_counts_challenges_once(challenge, player_factory, fresh_team):
    other_challenge = Challenge(points=300, name="Challenge2")
    other_challenge.save()
    other_team = Team(name="Team with Score", creator=player_factory.get())
    other_team.save()
    member = Player(username='player', password='', team=other_team)
    member.save()
    Solution(challenge=challenge, solver=member).save()
    Solution(challenge=challenge, solver=other_team.creator).save()
    Solution(challenge=other_challenge, solver=fresh_team.creator).save()
    leaderboard = Team.get_leaderboard()
    assert (leaderboard[0] == other_team and
            leaderboard[1] == fresh_team and
            len(leaderboard) == 2)


@pytest.mark.django_db
def test_leaderboard_sorts_by_points_and_time(challenge, player_factory, fresh_team):
    team1 = Team(name="1st Team with Score", creator=player_factory.get())
    team1.save()
    team2 = Team(name="2nd Team with Score", creator=player_factory.get())
    team2.save()
    member1 = Player(username='team1player', password='', team=team1)
    member1.save()
    member2 = Player(username='team2player', password='', team=team2)
    member2.save()
    Solution(challenge=challenge, solver=member2).save()
    Solution(challenge=challenge, solver=member1).save()
    leaderboard = Team.get_leaderboard()
    assert (leaderboard[0] == team2 and
            leaderboard[1] == team1 and
            leaderboard[2] == fresh_team and
            len(leaderboard) == 3)


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


@pytest.mark.django_db
def test_points(challenge, player_factory, fresh_team):
    assert fresh_team.points() == 0
    member = Player(username='player', password='', team=fresh_team)
    member.save()
    challenge.points = 100
    challenge.save()
    Solution(challenge=challenge, solver=member).save()
    assert fresh_team.points() == 100
