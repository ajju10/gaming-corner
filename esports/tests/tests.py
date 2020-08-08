from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core import mail
from django.test import TestCase
from django.utils import timezone

from esports.models import Tournament, Participant

today = timezone.now()


class HomePageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class UserAuthenticationTest(TestCase):

    def test_user_signup(self):
        user = get_user_model().objects.create(
                username='testuser',
                password='TestUser'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.password, 'TestUser')


class TournamentAndParticipantModelsTest(TestCase):

    def test_can_add_tournament_and_participant_models(self):
        first_tournament = Tournament.objects.create(
            name='This is a fake tournament',
            discipline='Fake PUBG Mobile',
            description='This is not a game at all. This is just for testing purposes.',
            is_team=False,
            size=100,
            organizer=get_user_model().objects.create(username='test', password='testuser'),
            start_time=today,
            end_time=today + timedelta(days=2)
        )

        second_tournament = Tournament.objects.create(
            name='This is not actually a tournament',
            discipline='Fake PUBG Lite',
            description='This is not a game at all. This is just for unit testing purposes.',
            is_team=True,
            size=25,
            organizer=get_user_model().objects.create(username='test1', password='testuser1'),
            start_time=today,
            end_time=today + timedelta(days=2)
        )

        tournaments = Tournament.objects.count()
        self.assertEqual(tournaments, 2)

        self.assertEqual(first_tournament.size, 100)
        self.assertEqual(second_tournament.size, 25)

        self.assertEqual(Tournament.get_planned_tournaments().count(), 2)
        self.assertEqual(Tournament.get_ongoing_tournaments().count(), 0)

        first_player = Participant.objects.create(
            email='first@xyz.com',
            tournament=Tournament.objects.first(),
            name='first',
            timestamp=today
        )
        self.assertEqual(first_tournament.remaining_slots(), 99)

        second_player = Participant.objects.create(
            email='second@xyz.com',
            tournament=Tournament.objects.last(),
            name='second',
            timestamp=today
        )
        self.assertEqual(second_tournament.remaining_slots(), 24)

        players = Participant.objects.count()
        self.assertEqual(players, 2)

        self.assertEqual(Participant.objects.first(), first_player)
        self.assertEqual(Participant.objects.last(), second_player)

        self.assertEqual(first_player.tournament, Tournament.objects.first())
        self.assertEqual(second_player.tournament, Tournament.objects.last())


class TournamentViewTest(TestCase):

    def test_uses_a_browse_template(self):
        response = self.client.get('/browse/')
        self.assertTemplateUsed(response, 'browse.html')

    def test_tournament_search_form(self):
        Tournament.objects.create(
            name='This is a fake tournament',
            discipline='Fake PUBG Mobile',
            description='This is not a game at all. This is just for testing purposes.',
            is_team=False,
            size=100,
            organizer=get_user_model().objects.create(username='test', password='testuser'),
            start_time=today,
            end_time=today + timedelta(days=2)
        )

        tournaments = Tournament.objects.count()
        self.assertEqual(tournaments, 1)

        response = self.client.get('/browse/', data={
            'q': 'fake'
        })

        self.assertEqual(response.status_code, 200)

    def test_tournament_details_view(self):
        Tournament.objects.create(
            name='This is a fake tournament',
            discipline='Fake PUBG Mobile',
            description='This is not a game at all. This is just for testing purposes.',
            is_team=False,
            size=100,
            organizer=get_user_model().objects.create(username='test', password='testuser'),
            start_time=today,
            end_time=today + timedelta(days=2)
        )
        self.assertEqual(Tournament.objects.count(), 1)

        Participant.objects.create(
            email='first@xyz.com',
            tournament=Tournament.objects.first(),
            name='first',
            timestamp=today
        )
        self.assertEqual(Participant.objects.count(), 1)

        tournament = Tournament.objects.first()
        participants = tournament.participant.all()

        self.assertIn(Participant.objects.first(), participants)


class NewTournamentTest(TestCase):

    def test_can_save_a_new_tournament_POST_request(self):
        response = self.client.post('/organize/new', data={
            'name': 'This is a fake tournament',
            'discipline': 'Fake PUBG Mobile',
            'description': 'This is not a game at all.',
            'is_team': False,
            'size': 100,
            'organizer': get_user_model().objects.create(username='User', password='Password'),
            'start_time': today,
            'end_time': today + timedelta(days=2)
        }, follow=True)
        self.assertEqual(response.status_code, 200)


class NewParticipantTest(TestCase):

    def test_can_save_a_new_participant_POST_request(self):
        tournament = Tournament.objects.create(
            name='This is a fake tournament',
            discipline='Fake PUBG Mobile',
            description='This is not a game at all. This is just for testing purposes.',
            is_team=False,
            size=100,
            organizer=get_user_model().objects.create(username='testparticipant', password='testuser'),
            start_time=today,
            end_time=today + timedelta(days=2)
        )

        self.assertEqual(Tournament.objects.count(), 1)

        response = self.client.post(f"/tournament/join/{tournament.id}", data={
            'email': 'test@test.com',
            'tournament': tournament,
            'name': 'player',
            'timestamp': today
        })

        self.assertEqual(response.status_code, 200)

    def test_user_cannot_register_in_a_tournament_twice(self):
        tournament = Tournament.objects.create(
            name='This is a fake tournament',
            discipline='Fake PUBG Mobile',
            description='This is not a game at all. This is just for testing purposes.',
            is_team=False,
            size=100,
            organizer=get_user_model().objects.create(username='testparticipant', password='testuser'),
            start_time=today,
            end_time=today + timedelta(days=2)
        )

        p1 = Participant.objects.create(
            email='test@test.com',
            tournament=tournament,
            name='admin'
        )

        self.assertEqual(Participant.objects.count(), 1)
        self.assertEqual(p1.tournament, tournament)
        # Complete this test


class SendEmailTest(TestCase):

    def test_can_send_an_email(self):
        mail.send_mail('Test subject', 'Test message', 'from@example.com', ['to@example.com'])

        self.assertEqual(len(mail.outbox), 1)

        self.assertEqual(mail.outbox[0].subject, 'Test subject')
