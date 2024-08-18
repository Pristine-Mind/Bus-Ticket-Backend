from datetime import timedelta

from django.conf import settings
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema
from google.auth.transport import requests
from google.oauth2 import id_token
from rest_framework import response, status, views
from rest_framework.authtoken.models import Token

from user.models import User

from .serializers import LoginSerializer, RegisterSerializer


def bad_request(message):
    return JsonResponse({"statusCode": 400, "error_message": message}, status=400)


@extend_schema(request=None, responses=RegisterSerializer)
class RegistrationView(views.APIView):

    def post(self, request, version=None):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(request=None, responses=LoginSerializer)
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


@csrf_exempt
def dev_sign_in(request):
    """
    For server-side development only, Used to simulate frontend sign_in
    """
    return render(
        request,
        "common/sign_in.html",
        context=dict(
            GOOGLE_OAUTH_CLIENT_ID=settings.GOOGLE_OAUTH_CLIENT_ID,
            GOOGLE_OAUTH_REDIRECT_URL=settings.GOOGLE_OAUTH_REDIRECT_URL,
        ),
    )


@csrf_exempt
def google_oauth(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    error_postfix = (
        f"</br> Go back to the application here: <a href='{settings.APP_FRONTEND_HOST}'>{settings.APP_FRONTEND_HOST}</a>"
    )
    if request.method.upper() == "GET":
        return HttpResponse(
            f"Not sure what you are trying to do here {error_postfix}",
            status=405,
        )

    token = request.POST.get("credential")

    if token is None:
        return HttpResponse(
            f"No credential provided {error_postfix}",
            status=400,
        )

    try:
        user_data = id_token.verify_oauth2_token(token, requests.Request(), settings.GOOGLE_OAUTH_CLIENT_ID)
        if user_data["email_verified"] is not True:
            return HttpResponse(
                "Email is not verified {error_postfix}",
                status=400,
            )
    except ValueError:
        return HttpResponse(
            f"Failed to process {error_postfix}",
            status=403,
        )

    email = user_data["email"].lower()
    if user := User.objects.filter(email=email).first():
        user.first_name = user_data["given_name"]
        user.last_name = user_data["family_name"]
        user.save(update_fields=("first_name", "last_name"))
        login(request, user)
    else:
        new_user = User.objects.create(
            email=email,
            first_name=user_data["given_name"],
            last_name=user_data["family_name"],
        )
        login(request, new_user)

    return redirect(settings.APP_FRONTEND_HOST)
