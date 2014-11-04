from django.contrib import admin
from core.models import Challenge, Hint, Team, Player, Solution
from core.forms import ChallengeAdminForm


class ChallengeAdmin(admin.ModelAdmin):
    fields = ['name', 'points', 'category', 'flag', 'description_markdown']
    form = ChallengeAdminForm

class HintAdmin(admin.ModelAdmin):
    fields = ['challenge', 'content_markdown', 'publish_date']

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(Hint, HintAdmin)
admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Solution)
