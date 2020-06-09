from django.contrib import messages
from django.shortcuts import render, redirect
from .models import Tournament
from .forms import OrganizeTournamentForm


def home(request):
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})


def organize_new(request):
    if request.method == "POST":
        form = OrganizeTournamentForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'Tournament has been successfully created.')
            return redirect('my_tournaments')
    else:
        form = OrganizeTournamentForm()
        return render(request, 'organize_new.html', {'form': form})


def my_tournaments(request):
    tournaments = Tournament.objects.all()
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
            query = Tournament.objects.filter(name__startswith=tournament_name)
        except Exception as e:
            query = "Error"
            print('Not found')
        return render(request, 'browse.html', {'query': query})
    else:
        tournaments = Tournament.objects.all()
        return render(request, 'browse.html', {'tournaments': tournaments})
