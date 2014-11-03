from django.conf.urls import patterns, include, url
from tastypie.api import Api
from core import api

v1_api = Api(api_name='v1')
v1_api.register(api.ChallengeResource())
v1_api.register(api.PlayerResource())
v1_api.register(api.SolutionResource())
v1_api.register(api.TeamResource())

urlpatterns = patterns('',
    (r'^api/', include(v1_api.urls)),
)
