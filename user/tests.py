from unittest.mock import patch

from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory
from django.urls import reverse

from main.tests import TestCase
from user.factories import UserFactory
from user.models import User
from user.views import google_oauth


class TestGoogleOAuth(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.mock_oauth2_valid_response = {
            "hd": "test.com",
            "email": "test@test.com",
            "email_verified": True,
            "given_name": "Test",
            "family_name": "Last",
        }
        UserFactory.create_batch(3)  # Noise data

    @patch("user.views.id_token.verify_oauth2_token")
    def test_sign_up(self, verify_oauth2_token_mock):
        request = self.factory.post(
            reverse("google_oauth"),
            data={"credential": "who you"},
        )
        middleware = SessionMiddleware(self.no_op)
        middleware.process_request(request)
        request.session.save()

        def _query_count_check(count):
            assert User.objects.filter(email=self.mock_oauth2_valid_response["email"]).count() == count

        _query_count_check(0)
        assert list(request.session.items()) == []

        # Failure response 01
        verify_oauth2_token_mock.return_value = {
            **self.mock_oauth2_valid_response,
            "email_verified": False,
        }
        response = google_oauth(request)
        assert response.status_code == 400
        assert list(request.session.items()) == []
        _query_count_check(0)

        # Failure response 02
        verify_oauth2_token_mock.side_effect = lambda *_: (_ for _ in ()).throw(ValueError("Random error"))
        response = google_oauth(request)
        assert response.status_code == 403
        assert list(request.session.items()) == []
        _query_count_check(0)

        # Success response
        verify_oauth2_token_mock.reset_mock(side_effect=True)
        verify_oauth2_token_mock.return_value = {**self.mock_oauth2_valid_response}
        response = google_oauth(request)
        assert response.status_code == 302
        assert list(request.session.items()) != []
        assert len(list(request.session.items())) == 3
        assert list(request.session.items())[0] == (
            "_auth_user_id",
            str(User.objects.get(email=self.mock_oauth2_valid_response["email"]).pk),
        )
        _query_count_check(1)

    @patch("user.views.id_token.verify_oauth2_token")
    def test_sign_in(self, verify_oauth2_token_mock):
        user = UserFactory.create(email=self.mock_oauth2_valid_response["email"])
        UserFactory.create_batch(3)

        request = self.factory.post(
            reverse("google_oauth"),
            data={"credential": "XYZ"},
        )
        middleware = SessionMiddleware(self.no_op)
        middleware.process_request(request)
        request.session.save()

        # Failure response 01
        verify_oauth2_token_mock.return_value = {
            **self.mock_oauth2_valid_response,
            "email_verified": False,
        }
        response = google_oauth(request)
        assert list(request.session.items()) == []
        assert response.status_code == 400

        # Failure response 02
        verify_oauth2_token_mock.side_effect = lambda *_: (_ for _ in ()).throw(ValueError("Random error"))
        response = google_oauth(request)
        assert list(request.session.items()) == []
        assert response.status_code == 403

        # Success response
        verify_oauth2_token_mock.reset_mock(side_effect=True)
        verify_oauth2_token_mock.return_value = {**self.mock_oauth2_valid_response}
        response = google_oauth(request)
        assert list(request.session.items()) != []
        assert len(list(request.session.items())) == 3
        assert list(request.session.items())[0] == ("_auth_user_id", str(user.pk))
        assert response.status_code == 302
