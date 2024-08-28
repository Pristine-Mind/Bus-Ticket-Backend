from rest_framework import viewsets
from rest_framework.response import Response

from .models import Booking, BookingDetail, Bus, BusRoute, Route
from .serializers import (
    BookingDetailSerializer,
    BookingSerializer,
    BusRouteSerializer,
    BusSerializer,
    RouteSerializer,
)


class BusViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing bus instances.
    """

    queryset = Bus.objects.all()
    serializer_class = BusSerializer
    filterset_fields = ["bus_type", "availability_status"]
    search_fields = ["bus_number"]
    ordering_fields = ["bus_number", "capacity"]


class RouteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for viewing and editing route instances.
    """

    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    search_fields = ["start_location", "end_location"]
    ordering_fields = ["start_location", "end_location", "scheduled_time"]


class BusRouteViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing bus route instances.
    """

    queryset = BusRoute.objects.all()
    serializer_class = BusRouteSerializer
    filterset_fields = ["date", "bus__bus_type", "route__start_location", "route__end_location"]
    search_fields = ["bus__bus_number", "route__start_location", "route__end_location"]
    ordering_fields = ["date", "available_seats"]


class BookingViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking instances.
    """

    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    filterset_fields = ["user__username", "booking_time"]
    search_fields = ["user__username"]
    ordering_fields = ["booking_time"]

    def create(self, request, *args, **kwargs):
        """
        Override create to handle nested BookingDetail data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)


class BookingDetailViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing booking detail instances.
    """

    queryset = BookingDetail.objects.all()
    serializer_class = BookingDetailSerializer
    filterset_fields = ["bus_route__date", "bus_route__bus__bus_type", "bus_route__route__start_location"]
    search_fields = ["bus_route__bus__bus_number", "bus_route__route__start_location", "bus_route__route__end_location"]
    ordering_fields = ["bus_route__date"]
