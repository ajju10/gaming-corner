from django import forms

from .models import Tournament


class TournamentSearchForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name']


class OrganizeTournamentForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'description', 'discipline', 'is_team', 'size']
