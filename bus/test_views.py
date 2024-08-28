from rest_framework import status
from rest_framework.test import APITestCase

from .factories import (
    BookingFactory,
    BusFactory,
    BusRouteFactory,
    RouteFactory,
    UserFactory,
)
from .models import Booking, BusRoute


class BusAPITestCase(APITestCase):

    def test_get_bus_list(self):
        BusFactory.create_batch(3)
        response = self.client.get("/api/v1/buses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_get_route_list(self):
        RouteFactory.create_batch(4)
        response = self.client.get("/api/v1/routes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 4)

    def test_get_bus_route_list(self):
        BusRouteFactory.create_batch(5)
        response = self.client.get("/api/v1/bus-routes/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_bus_route(self):
        bus = BusFactory.create()
        route = RouteFactory.create()
        data = {"bus": bus.id, "route": route.id, "date": "2024-08-01", "available_seats": 20}
        response = self.client.post("/api/v1/bus-routes/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BusRoute.objects.count(), 1)

    def test_get_booking_list(self):
        BookingFactory.create_batch(5)
        response = self.client.get("/api/v1/bookings/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 5)

    def test_create_booking(self):
        user = UserFactory()
        bus_route = BusRouteFactory()
        data = {"user": user.id, "book": [{"bus_route": bus_route.id, "seat_numbers": 3}]}
        response = self.client.post("/api/v1/bookings/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Booking.objects.count(), 1)
