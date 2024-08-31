from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db import models

from phonenumber_field.modelfields import PhoneNumberField


class Reservation(models.Model):
    """
    A model representing a reservation for a vehicle journey.

    Attributes
    ----------
    name : str
        The full name of the person making the reservation.
    mobile_no : str
        The mobile number of the person making the reservation. Must be numeric and at least 10 digits long.
    date_of_travel : date
        The date on which the journey is scheduled to take place.
    duration_type : str
        The type of duration for the journey. Choices are 'Day Based' or 'Hourly Based'.
    passenger_numbers : int
        The number of passengers included in the reservation.
    journey_from : str
        The starting location of the journey. Must be a different city than `journey_to`.
    journey_to : str
        The destination of the journey. Must be a different city than `journey_from`.
    vehicle_type : str
        The type of vehicle requested for the journey. Choices include 'Bus', 'Minivan', or 'Car'.
    comment : str, optional
        Any additional comments or specifications provided by the person making the reservation.

    Methods
    -------
    clean():
        Validates that the `journey_from` and `journey_to` are different, the `date_of_travel` is not in the past
    """

    class DurationType(models.TextChoices):
        DAY_BASED = 'day_based', 'Day Based'
        HOURLY_BASED = 'hourly_based', 'Hourly Based'

    class VehicleType(models.TextChoices):
        BUS = 'bus', 'Bus'
        MINIVAN = 'minivan', 'Minivan'
        CAR = 'car', 'Car'

    # TODO: Add seperate way to load city
    class CityChoices(models.TextChoices):
        KATHMANDU = 'kathmandu', 'Kathmandu'
        POKHARA = 'pokhara', 'Pokhara'
        LALITPUR = 'lalitpur', 'Lalitpur'
        BHAKTAPUR = 'bhaktapur', 'Bhaktapur'
        BIRATNAGAR = 'biratnagar', 'Biratnagar'
        BIRGUNJ = 'birgunj', 'Birgunj'
        DHARAN = 'dharan', 'Dharan'
        BHARATPUR = 'bharatpur', 'Bharatpur'
        BUTWAL = 'butwal', 'Butwal'
        HETAUDA = 'hetauda', 'Hetauda'
        JANAKPUR = 'janakpur', 'Janakpur'
        DHANGADHI = 'dhangadhi', 'Dhangadhi'
        NEPALGUNJ = 'nepalgunj', 'Nepalgunj'
        ITAHARI = 'itahari', 'Itahari'
        TULSIPUR = 'tulsipur', 'Tulsipur'
        SIDDHARTHANAGAR = 'siddharthanagar', 'Siddharthanagar (Bhairahawa)'
        GHORAHI = 'ghorahi', 'Ghorahi'
        DAMAK = 'damak', 'Damak'
        RAJBIRAJ = 'rajbiraj', 'Rajbiraj'
        LAHAN = 'lahan', 'Lahan'
        INARUWA = 'inaruwa', 'Inaruwa'
        TIKAPUR = 'tikapur', 'Tikapur'
        KIRTIPUR = 'kirtipur', 'Kirtipur'
        BHADRAPUR = 'bhadrapur', 'Bhadrapur'
        MECHINAGAR = 'mechinagar', 'Mechinagar (Kakarbhitta)'

    name = models.CharField(
        max_length=100,
        verbose_name="Full Name",
        help_text="Enter your full name."
    )
    mobile_no = PhoneNumberField(
        region="NP",
        verbose_name="Mobile Number",
        help_text="Enter your mobile number."
    )
    date_of_travel = models.DateField(
        verbose_name="Date of Travel",
        help_text="Select the date of your travel."
    )
    duration_type = models.CharField(
        max_length=12,
        choices=DurationType.choices,
        verbose_name="Duration Type",
        help_text="Select whether the duration is day-based or hourly-based."
    )
    passenger_numbers = models.PositiveIntegerField(
        verbose_name="Number of Passengers",
        help_text="Enter the number of passengers."
    )
    journey_from = models.CharField(
        max_length=100,
        choices=CityChoices.choices,
        verbose_name="Journey From",
        help_text="Select the starting location of your journey."
    )
    journey_to = models.CharField(
        max_length=100,
        choices=CityChoices.choices,
        verbose_name="Journey To",
        help_text="Select the destination of your journey."
    )
    vehicle_type = models.CharField(
        max_length=20,
        choices=VehicleType.choices,
        verbose_name="Vehicle Type",
        help_text="Select the type of vehicle for your journey."
    )
    comment = models.TextField(
        blank=True,
        null=True,
        verbose_name="Additional Comments",
        help_text="Enter any additional specifications or requests (optional)."
    )

    def clean(self):
        """
        Validates the reservation data.

        Raises
        ------
        ValidationError
            If `journey_from` and `journey_to` are the same.
            If `date_of_travel` is in the past.
        """
        if self.journey_from == self.journey_to:
            raise ValidationError('Journey From and Journey To cannot be the same.')

        if self.date_of_travel < timezone.now().date():
            raise ValidationError('Date of Travel cannot be in the past.')

    def __str__(self):
        """
        Returns a string representation of the reservation.

        Returns
        -------
        str
            The name of the person making the reservation and the date of travel.
        """
        return f"{self.name} - {self.date_of_travel}"
