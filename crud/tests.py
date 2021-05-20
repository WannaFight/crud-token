from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth.models import User


class UserListTests(APITestCase):
    url = reverse('crud:list')

    def setUp(self) -> None:
        user = User.objects.create_user(username='egg', password='egg')
        Token.objects.create(user=user)
        User.objects.create_user(username='spam', password='spam')

    def tearDown(self) -> None:
        User.objects.all().delete()
        Token.objects.all().delete()

    def test_get_with_auth(self):
        """
        Make sure we get HTTP 200 with token.
        """

        token = User.objects.get(username='egg').auth_token.key
        resp = self.client.get(
            self.url, **{'HTTP_AUTHORIZATION': f"Token {token}"}
        )

        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_with_no_auth(self):
        """
        Make sure we get HTTP 401 with no token.
        """
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_with_bad_auth(self):
        """
        Make sure we get HTTP 401 with bad token.
        """
        resp = self.client.get(self.url, **{'HTTP_AUTHORIZATION': f"Token !!"})

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_with_auth(self):
        """
        Make sure we get 201 with token.
        """
        token = User.objects.get(username='egg').auth_token.key
        data = {
            'username': 'guido',
            'password': '1234',
            'is_active': True,
        }
        resp = self.client.post(
            self.url, data=data, **{'HTTP_AUTHORIZATION': f"Token {token}"}
        )

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_post_with_no_token(self):
        """
        Make sure we get 401 with token.
        """
        data = {
            'username': 'guido',
            'password': '1234',
            'is_active': True
        }
        resp = self.client.post(self.url, data=data)

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailTest(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(username='egg', password='egg')
        Token.objects.create(user=user)
        User.objects.create_user(username='spam', password='spam')

    def tearDown(self) -> None:
        User.objects.all().delete()
        Token.objects.all().delete()

    def test_self_delete(self):
        """
        Make sure we can't delete ourselves and get HTTP 409
        """
        user = User.objects.get(username='egg')
        token, pk = user.auth_token.key, user.pk
        resp = self.client.delete(
            reverse('crud:detail', args=(pk,)),
            **{'HTTP_AUTHORIZATION': f"Token {token}"}
        )
        self.assertEqual(resp.status_code, status.HTTP_409_CONFLICT)

    def test_delete_with_auth(self):
        """
        Make sure we can delete users and get HTTP 204
        """
        pk = User.objects.get(username='spam').pk
        token = User.objects.get(username='egg').auth_token.key
        resp = self.client.delete(
            reverse('crud:detail', args=(pk,)),
            **{'HTTP_AUTHORIZATION': f"Token {token}"}
        )

        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_no_auth(self):
        pk = User.objects.get(username='egg').pk
        resp = self.client.delete(
            reverse('crud:detail', args=(pk,))
        )

        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)