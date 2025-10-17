from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Game

User = get_user_model()

class GameReviewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='g@test.com')
        self.user.set_password('Pwd12345!')
        self.user.save()
        token = self.client.post(reverse('token_obtain_pair'), {"email":"g@test.com","password":"Pwd12345!"}).data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    def test_create_game_and_review(self):
        # create game
        resp = self.client.post('/api/games/', {"title":"Test Game","slug":"test-game"})
        self.assertEqual(resp.status_code, 201)
        game_id = resp.data['id']
        # create review
        resp2 = self.client.post('/api/reviews/', {"game": game_id, "score": 8, "body": "Nice game!"})
        self.assertEqual(resp2.status_code, 201)
        self.assertEqual(resp2.data['score'], 8)
