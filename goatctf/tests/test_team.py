from django.db.utils import IntegrityError
import pytest

from core.models import Challenge, Player, Team, Solution


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
def user():
    user = Player()
    user.username = 'user'
    user.password = ''
    user.save()
    return user


@pytest.fixture
def fresh_team(user):
    Team.objects.all().delete()
    team = Team(name="Team", creator=user)
    team.save()
    return team


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


@pytest.mark.django_db
def test_leaderboard_empty_with_no_teams(challenge, user):
    assert len(Team.get_leaderboard()) == 0


@pytest.mark.django_db
def test_leaderboard_not_empty_with_one_team(challenge, user, fresh_team):
    leaderboard = Team.get_leaderboard()
    assert (leaderboard[0] == fresh_team and
            len(leaderboard) == 1)


@pytest.mark.django_db
def test_leaderboard_sorts_by_points(challenge, user, fresh_team):
    other_team = Team(name="Team with Score", creator=user)
    other_team.save()
    member = Player(username='player', password='', team=other_team)
    member.save()
    Solution(challenge=challenge, solver=member).save()
    leaderboard = Team.get_leaderboard()
    assert (leaderboard[0] == other_team and
            leaderboard[1] == fresh_team and
            len(leaderboard) == 2)


@pytest.mark.django_db
def test_leaderboard_sorts_by_points_and_time(challenge, user, fresh_team):
    team1 = Team(name="1st Team with Score", creator=user)
    team1.save()
    team2 = Team(name="2nd Team with Score", creator=user)
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
