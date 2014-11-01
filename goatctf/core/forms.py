from django import forms
from django.contrib.admin.widgets import AdminTextareaWidget


class ChallengeAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChallengeAdminForm, self).__init__(*args, **kwargs)
        self.fields['description_markdown'].widget = AdminTextareaWidget()
