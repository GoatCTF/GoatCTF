from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource
from core.models import Challenge, Team, Player, Solution 

class PlayerResource(ModelResource):
    full_name = fields.CharField('get_full_name')
    gravatar_url = fields.FileField('get_gravatar_url')
    has_gravatar = fields.BooleanField('has_gravatar')

    class Meta:
        queryset = Player.objects.all()
        resource_name = 'player'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        allowed_methods = ['get']


class TeamResource(ModelResource):
    members = fields.ToManyField(PlayerResource, 'player_set')

    class Meta:
        queryset = Team.objects.all()
        resource_name = 'team'
        allowed_methods = ['get']

class ChallengeResource(ModelResource):
    category_full = fields.CharField('get_category_display')

    class Meta:
        queryset = Challenge.objects.all()
        resource_name = 'challenge'
        allowed_methods = ['get']


class SolutionResource(ModelResource):
    challenge = fields.ForeignKey(ChallengeResource, 'challenge')
    player = fields.ForeignKey(PlayerResource, 'player')

    class Meta:
        queryset = Solution.objects.all()
        resource_name = 'solution'
        allowed_methods = ['get']

