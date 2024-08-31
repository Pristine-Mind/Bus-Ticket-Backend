"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from bus.views import (
    BookingDetailViewSet,
    BookingViewSet,
    BusRouteViewSet,
    BusViewSet,
    RouteViewSet,
)
from user.views import (
    LoginView,
    RegistrationView,
    UserViewSet,
    dev_sign_in,
    google_oauth,
)
from review.views import FeedbackReviewViewSet, FAQViewSet
from rental.views import ReservationCreateView

router = routers.DefaultRouter()

router.register(r"users", UserViewSet, basename="users")
router.register(r"buses", BusViewSet, basename="buses")
router.register(r"routes", RouteViewSet, basename="routes")
router.register(r"bus-routes", BusRouteViewSet, basename="bus-routes")
router.register(r"bookings", BookingViewSet, basename="bookings")
router.register(r"booking-details", BookingDetailViewSet, basename="booking-details")
router.register(r'feedback-reviews', FeedbackReviewViewSet, basename='feedback-review')
router.register(r'faqs', FAQViewSet, basename='faq')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("dev/sign_in/", dev_sign_in, name="dev-sign-in"),
    path("api/v1/", include(router.urls)),
    path("o/google", google_oauth, name="google_oauth"),
    path("register", RegistrationView.as_view()),
    path("login", LoginView.as_view()),
    path('reservations/', ReservationCreateView.as_view(), name='reservation-create'),
    # Docs
    path("docs/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api-docs/", SpectacularAPIView.as_view(), name="schema"),
    path("api-docs/swagger-ui/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
