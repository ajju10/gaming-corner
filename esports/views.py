from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import OrganizeTournamentForm, JoinTournamentForm
from .models import Tournament, Participant


def home(request):
    return render(request, 'home.html', {})


def about(request):
    return render(request, 'about.html', {})


@login_required
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


@login_required
def my_tournaments(request):
    organized_tournaments = Tournament.objects.filter(organizer=request.user)
    participated_tournaments = Participant.objects.filter(email__exact=request.user.email)
    return render(request, 'my_tournaments.html', {'organized_tournaments': organized_tournaments,
                                                   'participated_tournaments': participated_tournaments})


@login_required
def delete(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    tournament.delete()
    messages.success(request, 'Tournament has been successfully deleted.')
    return redirect('my_tournaments')


def browse(request):
    query = request.GET.get('q')
    if query:
        try:
            queryset_list = Tournament.objects.filter(Q(name__icontains=query) | Q(discipline__icontains=query))
        except Http404 as e:
            print(e)
            queryset_list = "Error"
        return render(request, 'browse.html', {'queryset_list': queryset_list})
    else:
        tournaments = Tournament.objects.all()
        return render(request, 'browse.html', {'tournaments': tournaments})


@login_required
def details(request, tournament_id):
    tournament = Tournament.objects.get(pk=tournament_id)
    return render(request, 'details.html', {'tournament': tournament})


def join_tournament(request, tournament_id):
    user = request.user
    tournament = Tournament.objects.get(pk=tournament_id)

    if request.method == 'POST':
        form = JoinTournamentForm(request.POST or None)

        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully joined this tournament. Please contact your organizer '
                                      'for further match instructions.')
            return redirect('my_tournaments')

    else:
        form = JoinTournamentForm(initial={'tournament': tournament.id})

    return render(request, 'join_tournament.html', {'user': user, 'tournament': tournament, 'form': form})
