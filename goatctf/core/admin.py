from django.contrib import admin
from core.models import Challenge, Team, Player, Solution
from core.forms import ChallengeAdminForm


class ChallengeAdmin(admin.ModelAdmin):
    fields = ['points', 'category', 'flag', 'description_markdown']
    form = ChallengeAdminForm

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Solution)
