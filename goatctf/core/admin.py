from django.contrib import admin
from core.models import Challenge
from core.forms import ChallengeAdminForm


class ChallengeAdmin(admin.ModelAdmin):
    fields = ['points', 'category', 'flag', 'description_markdown']
    form = ChallengeAdminForm

admin.site.register(Challenge, ChallengeAdmin)
