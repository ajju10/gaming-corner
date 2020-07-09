from django import forms

from .models import Tournament, Participant


class CustomDateTimeInput(forms.DateTimeInput):
    input_type = 'datetime-local'


class TournamentSearchForm(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name']


class OrganizeTournamentForm(forms.ModelForm):

    end_time = forms.DateTimeField(
        input_formats=['%d-%m-%Y %H:%M'],
        widget=forms.DateTimeInput(format='%d-%m-%Y %H:%M'),
    )

    class Meta:
        model = Tournament
        fields = ['name', 'description', 'discipline', 'is_team', 'size', 'end_time']


class JoinTournamentForm(forms.ModelForm):

    class Meta:
        model = Participant
        widgets = {'tournament': forms.HiddenInput()}
        fields = ['email', 'tournament', 'name']
