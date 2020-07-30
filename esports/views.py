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


def contact_us(request):
    return render(request, 'contact_us.html', {})


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
            messages.error(request, 'Form values are invalid. Please enter valid values.')
    else:
        form = OrganizeTournamentForm()
    return render(request, 'organize_new.html', {'form': form})


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
            queryset_list = Tournament.get_planned_tournaments().filter(
                Q(name__icontains=query) | Q(discipline__icontains=query))
        except Http404 as e:
            print(e)
            queryset_list = "Error"
        return render(request, 'browse.html', {'queryset_list': queryset_list})
    else:
        joinable_tournaments = Tournament.get_planned_tournaments().all()
        return render(request, 'browse.html', {'joinable_tournaments': joinable_tournaments})


@login_required
def details(request, tournament_id):
    tournament = Tournament.get_planned_tournaments().get(pk=tournament_id)
    participants = tournament.participant.all()
    try:
        registered_user = tournament.participant.get(email__exact=request.user.email)
    except Exception as e:
        print(e)
        registered_user = "Error"
    return render(request, 'details.html', {'tournament': tournament,
                                            'registered_user': registered_user,
                                            'participants': participants})


def join_tournament(request, tournament_id):
    tournament = Tournament.get_planned_tournaments().get(pk=tournament_id)
    try:
        registered_user = tournament.participant.get(email__exact=request.user.email)
    except Exception as e:
        print(e)
        registered_user = "Error"

    if request.method == 'POST':
        form = JoinTournamentForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have successfully joined this tournament. Please contact your organizer '
                                      'for further match instructions.')
            return redirect('browse')
    else:
        form = JoinTournamentForm(initial={'tournament': tournament.id})
    return render(request, 'join_tournament.html', {'tournament': tournament,
                                                    'form': form,
                                                    'registered_user': registered_user})
