from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from esports.forms import OrganizeTournamentForm, JoinTournamentForm
from esports.models import Tournament, Participant

today = timezone.now()


class ItemFormTest(TestCase):

    def test_organize_tournament_form_creates_new_tournament(self):
        form = OrganizeTournamentForm({
            'name': 'Test tournament',
            'description': 'This is a test tournament',
            'discipline': 'PUBG Mobile',
            'is_team': False,
            'size': 100,
            'end_time': today + timedelta(days=2)
        })
        self.assertTrue(form.is_valid())
        f = form.save(commit=False)
        f.organizer = get_user_model().objects.create(
            username='testuser',
            password='TestUser'
        )
        f.save()
        self.assertEqual(Tournament.objects.count(), 1)
        tournament = Tournament.objects.first()

        self.assertEqual(tournament.name, "Test tournament")
        self.assertEqual(tournament.description, 'This is a test tournament')
        self.assertEqual(tournament.discipline, 'PUBG Mobile')
        self.assertFalse(tournament.is_team)
        self.assertEqual(tournament.size, 100)
        self.assertEqual(tournament.end_time, today + timedelta(days=2))
        self.assertFalse(tournament.is_full())
        self.assertIn(tournament, Tournament.get_planned_tournaments())
        self.assertNotIn(tournament, Tournament.get_ongoing_tournaments())
        self.assertNotIn(tournament, Tournament.past_tournaments())

    def test_blank_data_in_organize_tournament_form(self):
        form = OrganizeTournamentForm()
        self.assertFalse(form.is_valid())

    def test_join_tournament_form_joins_new_tournament(self):
        form = JoinTournamentForm({
            'email': 'test@xyz.com',
            'tournament': Tournament.objects.create(
                name='This is a fake tournament',
                discipline='Fake PUBG Mobile',
                description='This is not a game at all. This is just for testing purposes.',
                is_team=False,
                size=100,
                organizer=get_user_model().objects.create(username='test', password='testuser'),
                start_time=today,
                end_time=today + timedelta(days=2)
            ),
            'name': 'test player'
        })
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(Participant.objects.count(), 1)
        participant = Participant.objects.first()

        self.assertEqual(participant.name, 'test player')
        self.assertEqual(participant.email, 'test@xyz.com')
        self.assertEqual(participant.tournament, Tournament.objects.first())

    def test_blank_data_in_join_tournament_form(self):
        form = JoinTournamentForm()
        self.assertFalse(form.is_valid())
