import factory
from factory.django import DjangoModelFactory

from django.utils import timezone

from user.models import User
from .models import (
    Bus,
    Route,
    BusRoute,
    Booking,
    BookingDetail,
)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'dummyuser{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class BusFactory(DjangoModelFactory):
    class Meta:
        model = Bus

    bus_number = factory.Sequence(lambda n: f'BUS{n:03d}')
    bus_type = factory.Iterator([Bus.BusType.AC, Bus.BusType.NON_AC])
    capacity = factory.Faker('random_int', min=30, max=60)
    availability_status = factory.Faker('boolean')


class RouteFactory(DjangoModelFactory):
    class Meta:
        model = Route

    start_location = factory.Sequence(lambda n: f'City {chr(65 + n)}')
    end_location = factory.Sequence(lambda n: f'City {chr(66 + n)}')
    stops = factory.LazyAttribute(lambda obj: 'Stop 1, Stop 2, Stop 3')
    scheduled_time = factory.LazyFunction(timezone.now().time)


class BusRouteFactory(DjangoModelFactory):
    class Meta:
        model = BusRoute

    bus = factory.SubFactory(BusFactory)
    route = factory.SubFactory(RouteFactory)
    date = factory.Faker('date_this_month')
    available_seats = factory.Faker('random_int', min=10, max=50)


class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    booking_time = factory.LazyFunction(timezone.now)


class BookingDetailFactory(DjangoModelFactory):
    class Meta:
        model = BookingDetail

    bus_route = factory.SubFactory(BusRouteFactory)
    seat_numbers = factory.Faker('random_int', min=1, max=5)
