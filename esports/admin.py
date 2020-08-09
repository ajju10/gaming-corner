from django.contrib import admin
from .models import Tournament, Participant


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'organizer', 'size', 'is_team']
    list_filter = ['discipline', 'is_team', 'organizer']


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'tournament']
    list_filter = ['tournament']


admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Participant, ParticipantAdmin)
