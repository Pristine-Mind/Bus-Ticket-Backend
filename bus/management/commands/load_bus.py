import random

from django.core.management.base import BaseCommand
from django.utils import timezone

from bus.models import Booking, BookingDetail, Bus, BusRoute, Route
from user.models import User


class Command(BaseCommand):
    help = "Load dummy bus data"

    def handle(self, *args, **kwargs):

        buses = []
        for i in range(20):
            bus_number = f"BUS{i+1:03d}"
            bus_type = random.choice([Bus.BusType.AC, Bus.BusType.NON_AC])
            capacity = random.randint(30, 60)
            availability_status = random.choice([True, False])
            bus = Bus.objects.create(
                bus_number=bus_number, bus_type=bus_type, capacity=capacity, availability_status=availability_status
            )
            buses.append(bus)
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(buses)} buses!"))

        routes = []
        for i in range(20):
            start_location = f"City {chr(65 + i)}"
            end_location = f"City {chr(66 + i)}"
            stops = f"Stop {i*3+1}, Stop {i*3+2}, Stop {i*3+3}"
            scheduled_time = (timezone.now() + timezone.timedelta(minutes=i * 15)).time()
            route = Route.objects.create(
                start_location=start_location, end_location=end_location, stops=stops, scheduled_time=scheduled_time
            )
            routes.append(route)
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(routes)} routes!"))

        bus_routes = []
        for i in range(50):
            bus = random.choice(buses)
            route = random.choice(routes)
            date = timezone.now().date() + timezone.timedelta(days=i % 10)
            available_seats = random.randint(10, bus.capacity)
            bus_route = BusRoute.objects.create(bus=bus, route=route, date=date, available_seats=available_seats)
            bus_routes.append(bus_route)
        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {len(bus_route)} bus routes!"))

        users = []
        for i in range(10):
            username = f"dummyuser{i+1:02d}"
            email = f"{username}@example.com"
            password = "password"
            user = User.objects.create_user(username=username, email=email, password=password)
            users.append(user)

        for i in range(20):
            user = random.choice(users)
            booking = Booking.objects.create(user=user, booking_time=timezone.now())

            # Create 2 to 5 booking details per booking
            booking_details = []
            for j in range(random.randint(2, 5)):
                bus_route = random.choice(bus_routes)
                seat_numbers = random.randint(1, bus_route.available_seats)
                booking_detail = BookingDetail.objects.create(bus_route=bus_route, seat_numbers=seat_numbers)
                booking_details.append(booking_detail)

            booking.book.add(*booking_details)

        self.stdout.write(self.style.SUCCESS("Successfully loaded entries!!"))
