from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import OrganizeTournamentForm
from .models import Tournament


def home(request):
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})


@login_required()
def organize_new(request):
    if request.method == "POST":
        form = OrganizeTournamentForm(request.POST or None)

        if form.is_valid():
            f = form.save(commit=False)
            f.organizer = request.user
            f.save()
            messages.success(request, 'Tournament has been successfully created.')
            return redirect('my_tournaments')
    else:
        form = OrganizeTournamentForm()
    return render(request, 'organize_new.html', {'form': form, })


@login_required()
def my_tournaments(request):
    tournaments = Tournament.objects.filter(organizer=request.user)
    return render(request, 'my_tournaments.html', {'tournaments': tournaments})


def delete(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    tournament.delete()
    messages.success(request, 'Tournament has been successfully deleted.')
    return redirect('my_tournaments')


def browse(request):
    if request.method == 'POST':
        tournament_name = request.POST['game_name']
        try:
            query = Tournament.objects.filter(name__icontains=tournament_name)
        except Http404:
            query = "Not such tournament found"
        return render(request, 'browse.html', {'query': query})
    else:
        tournaments = Tournament.objects.all()
        return render(request, 'browse.html', {'tournaments': tournaments})


def register(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    return render(request, 'register.html', {'tournament': tournament})
