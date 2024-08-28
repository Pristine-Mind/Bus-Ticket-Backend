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
        AC = "ac", _("Air Conditioned")
        NON_AC = "non_ac", _("Non Air Conditioned")

    bus_number = models.CharField(
        max_length=20, unique=True, verbose_name=_("Bus Number"), help_text=_("Unique identifier for the bus (e.g., ABC123).")
    )
    bus_type = models.CharField(
        max_length=20,
        choices=BusType.choices,
        default=BusType.NON_AC,
        verbose_name=_("Bus Type"),
        help_text=_("Type of the bus (e.g., Air Conditioned, Sleeper)."),
    )
    capacity = models.IntegerField(verbose_name=_("Capacity"), help_text=_("Total number of seats available on the bus."))
    availability_status = models.BooleanField(
        default=True, verbose_name=_("Availability Status"), help_text=_("Indicates whether the bus is available for booking.")
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
        max_length=100, verbose_name=_("Start Location"), help_text=_("Starting point of the bus route.")
    )
    end_location = models.CharField(max_length=100, verbose_name=_("End Location"), help_text=_("Ending point of the bus route."))
    stops = models.TextField(verbose_name=_("Stops"), help_text=_("Comma separated list of intermediate stops."))
    scheduled_time = models.TimeField(verbose_name=_("Scheduled Time"), help_text=_("Scheduled departure time of the bus."))

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

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name=_("Bus"), help_text=_("Select the bus for this route."))
    route = models.ForeignKey(
        Route, on_delete=models.CASCADE, verbose_name=_("Route"), help_text=_("Select the route for this bus.")
    )
    date = models.DateField(verbose_name=_("Date"), help_text=_("Date on which the bus is scheduled for this route."))
    available_seats = models.IntegerField(
        verbose_name=_("Available Seats"), help_text=_("Number of seats available for booking on this bus.")
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

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_("User"), help_text=_("The user making the booking."))
    booking_time = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Booking Time"), help_text=_("Time when the booking was made.")
    )
    book = models.ManyToManyField(
        "BookingDetail",
        verbose_name=_("Book"),
        help_text=_("Multiple bookings for different routes."),
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
        BusRoute, on_delete=models.CASCADE, verbose_name=_("Bus Route"), help_text=_("The specific bus and route being booked.")
    )
    seat_numbers = models.IntegerField(
        verbose_name=_("Seat Numbers"), help_text=_("The list of seat numbers assigned to the user for this route.")
    )

    def __str__(self):
        return f"{self.bus_route} - Seats: {self.seat_numbers}"
