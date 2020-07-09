from django.contrib import admin
from .models import Tournament, Participant, Team


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'tournament']


class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'discipline', 'size', 'end_time']


admin.site.register(Tournament, TournamentAdmin)

admin.site.register(Participant, ParticipantAdmin)

admin.site.register(Team)
