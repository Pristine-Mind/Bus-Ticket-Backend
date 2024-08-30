from django.test import TestCase

from .factories import (
    BookingDetailFactory,
    BookingFactory,
    BusFactory,
    BusRouteFactory,
    RouteFactory,
)
from .models import Booking, BookingDetail, Bus, BusRoute, Route


class BusModelTest(TestCase):
    def test_create_bus(self):
        bus = BusFactory()
        self.assertTrue(isinstance(bus, Bus))
        self.assertEqual(bus.__str__(), f"{bus.bus_number} - {bus.get_bus_type_display()}")


class RouteModelTest(TestCase):
    def test_create_route(self):
        route = RouteFactory()
        self.assertTrue(isinstance(route, Route))
        self.assertEqual(route.__str__(), f"{route.start_location} to {route.end_location}")


class BusRouteModelTest(TestCase):
    def test_create_bus_route(self):
        bus_route = BusRouteFactory()
        self.assertTrue(isinstance(bus_route, BusRoute))
        self.assertEqual(bus_route.__str__(), f"{bus_route.bus.bus_number} on {bus_route.route} - {bus_route.date}")


class BookingModelTest(TestCase):
    def test_create_booking(self):
        booking = BookingFactory()
        self.assertTrue(isinstance(booking, Booking))
        self.assertEqual(booking.__str__(), f"Booking by {booking.user.username}")


class BookingDetailModelTest(TestCase):
    def test_create_booking_detail(self):
        booking_detail = BookingDetailFactory()
        self.assertTrue(isinstance(booking_detail, BookingDetail))
