import factory
from .models import Reservation


class ReservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reservation

    name = factory.Faker("name")
    mobile_no = factory.Faker("phone_number", locale="ne_NP")
    date_of_travel = factory.Faker("future_date")
    duration_type = factory.Iterator([Reservation.DurationType.DAY_BASED, Reservation.DurationType.HOURLY_BASED])
    passenger_numbers = factory.Faker("random_int", min=1, max=50)
    journey_from = factory.Iterator([choice[0] for choice in Reservation.CityChoices.choices])
    journey_to = factory.Iterator([choice[0] for choice in Reservation.CityChoices.choices])
    vehicle_type = factory.Iterator(
        [Reservation.VehicleType.BUS, Reservation.VehicleType.MINIVAN, Reservation.VehicleType.CAR]
    )
    comment = factory.Faker("sentence")
