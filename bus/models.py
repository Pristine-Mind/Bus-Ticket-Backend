from django.db import models
from django.utils.translation import gettext_lazy as _

from user.models import User


class Bus(models.Model):
    """
    Model representing a bus.

    Attributes
    ----------
    bus_number : str
        Unique identifier for the bus (e.g., ABC123).
    bus_type : str
        Type of the bus (e.g., Air Conditioned, Sleeper).
    capacity : int
        Total number of seats available on the bus.
    availability_status : bool
        Indicates whether the bus is available for booking.
    """

    class BusType(models.TextChoices):
        """
        Enumeration for different types of buses.

        Attributes
        ----------
        AC : str
            Air Conditioned bus.
        NON_AC : str
            Non Air Conditioned bus.
        """

        AC = "ac", "Air Conditioned"
        NON_AC = "non_ac", "Non Air Conditioned"

    bus_number = models.CharField(
        max_length=20, unique=True, verbose_name="Bus Number", help_text="Unique identifier for the bus (e.g., ABC123)."
    )
    bus_type = models.CharField(
        max_length=20,
        choices=BusType.choices,
        default=BusType.NON_AC,
        verbose_name="Bus Type",
        help_text="Type of the bus (e.g., Air Conditioned, Sleeper).",
    )
    capacity = models.IntegerField(verbose_name="Capacity", help_text="Total number of seats available on the bus.")
    availability_status = models.BooleanField(
        default=True, verbose_name="Availability Status", help_text="Indicates whether the bus is available for booking."
    )

    def __str__(self):
        return f"{self.bus_number} - {self.get_bus_type_display()}"


class Route(models.Model):
    """
    Model representing a bus route.

    Attributes
    ----------
    start_location : str
        Starting point of the bus route.
    end_location : str
        Ending point of the bus route.
    stops : str
        Comma-separated list of intermediate stops.
    scheduled_time : datetime.time
        Scheduled departure time of the bus.
    """

    start_location = models.CharField(
        max_length=100, verbose_name="Start Location", help_text="Starting point of the bus route."
    )
    end_location = models.CharField(max_length=100, verbose_name="End Location", help_text="Ending point of the bus route.")
    stops = models.TextField(verbose_name="Stops", help_text="Comma separated list of intermediate stops.")
    scheduled_time = models.TimeField(verbose_name="Scheduled Time", help_text="Scheduled departure time of the bus.")

    def __str__(self):
        return f"{self.start_location} to {self.end_location}"


class BusRoute(models.Model):
    """
    Model representing a bus assignment to a specific route on a specific date.

    Attributes
    ----------
    bus : Bus
        The bus assigned to the route.
    route : Route
        The route the bus is assigned to.
    date : datetime.date
        Date on which the bus is scheduled for this route.
    available_seats : int
        Number of seats available for booking on this bus.
    """

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name="Bus", help_text="Select the bus for this route.")
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, verbose_name="Route", help_text="Select the route for this bus."
    )
    date = models.DateField(verbose_name="Date", help_text="Date on which the bus is scheduled for this route.")
    available_seats = models.IntegerField(
        verbose_name="Available Seats", help_text="Number of seats available for booking on this bus."
    )

    def __str__(self):
        return f"{self.bus.bus_number} on {self.route} - {self.date}"


class Booking(models.Model):
    """
    Model representing a booking made by a user for multiple routes and seats.

    Attributes
    ----------
    user : User
        The user making the booking.
    booking_time : datetime.datetime
        Time when the booking was made.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User", help_text="The user making the booking.")
    booking_time = models.DateTimeField(
        auto_now_add=True, verbose_name="Booking Time", help_text="Time when the booking was made."
    )
    book = models.ManyToManyField(
        "BookingDetail",
        verbose_name=_("Book"),
        help_text=_("Multiple booking for different route"),
    )

    def __str__(self):
        return f"Booking by {self.user.username}"


class BookingDetail(models.Model):
    """
    Model representing the details of a booking, allowing multiple routes and seats in a single booking.

    Attributes
    ----------
    bus_route : BusRoute
        The specific bus and route being booked.
    seat_numbers : int
        The seat numbers assigned for this bus route.
    """

    bus_route = models.ForeignKey(
        BusRoute, on_delete=models.CASCADE, verbose_name="Bus Route", help_text="The specific bus and route being booked."
    )
    seat_numbers = models.IntegerField(
        verbose_name="Seat Numbers", help_text="The list of seat numbers assigned to the user for this route."
    )

    def __str__(self):
        return f"{self.booking.user.username} booking for {self.bus_route}"
