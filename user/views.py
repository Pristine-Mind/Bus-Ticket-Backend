from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

from rest_framework import (
    views,
    response,
    status
)
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegistrationSerializer,
    LoginSerializer,
)


def bad_request(message):
    return JsonResponse(
        {
            "statusCode": 400,
            "error_message": message
        },
        status=400
    )


@extend_schema(
    request=None,
    responses=RegistrationSerializer
)
class RegistrationView(views.APIView):

    def post(self, request, version=None):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(
            serializer.data, status=status.HTTP_200_OK
        )


@extend_schema(
    request=None,
    responses=LoginSerializer
)
class LoginView(views.APIView):
    permission_classes = []

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(email=email, password=password)
        if user is not None:
            api_key, created = Token.objects.get_or_create(user=user)

            # Reset the key's created_at time each time we get new credentials
            if not created:
                api_key.created = timezone.now()
                api_key.save()

            # TODO: Update profile as well

            return JsonResponse(
                {
                    "token": api_key.key,
                    "username": email,
                    "first": user.first_name,
                    "last": user.last_name,
                    "expires": api_key.created + timedelta(7),
                    "id": user.id,
                }
            )
        else:
            return bad_request("Invalid username or password")
