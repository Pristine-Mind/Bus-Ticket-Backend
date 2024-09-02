from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status
import factory

from .models import Reservation
from .factories import ReservationFactory


class ReservationAPITestCase(APITestCase):
    """
    Test case for the Reservation API.
    """

    def setUp(self):
        """
        Set up the test case with necessary data and configurations.
        """
        self.url = reverse("reservation-create")

    def test_create_reservation(self):
        """
        Test creating a reservation with valid data.
        """
        reservation_data = factory.build(dict, FACTORY_CLASS=ReservationFactory)
        reservation_data["mobile_no"] = "+9779853503420"

        # Ensure journey_from and journey_to are different
        if reservation_data["journey_from"] == reservation_data["journey_to"]:
            reservation_data["journey_to"] = (
                Reservation.CityChoices.POKHARA
                if reservation_data["journey_from"] != Reservation.CityChoices.POKHARA
                else Reservation.CityChoices.KATHMANDU
            )

        response = self.client.post(self.url, reservation_data, format="json")
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Reservation.objects.filter(name=reservation_data["name"]).exists())

    def test_create_reservation_invalid_date(self):
        """
        Test creating a reservation with an invalid (past) date.
        """
        reservation_data = factory.build(dict, FACTORY_CLASS=ReservationFactory)
        reservation_data["mobile_no"] = "+9779853503420"
        reservation_data["journey_to"] = Reservation.CityChoices.KATHMANDU
        reservation_data["journey_from"] = Reservation.CityChoices.BHAKTAPUR
        reservation_data["date_of_travel"] = "2020-10-20"

        response = self.client.post(self.url, reservation_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_reservation_same_journey(self):
        """
        Test creating a reservation where the journey_from and journey_to are the same.
        """
        reservation_data = factory.build(dict, FACTORY_CLASS=ReservationFactory)
        reservation_data["mobile_no"] = "+9779853503420"

        reservation_data["journey_to"] = reservation_data["journey_from"]

        response = self.client.post(self.url, reservation_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", response.data)

    def test_create_reservation_invalid_mobile(self):
        """
        Test creating a reservation with an invalid mobile number.
        """
        reservation_data = factory.build(dict, FACTORY_CLASS=ReservationFactory)
        reservation_data["mobile_no"] = "+9779853503420"

        reservation_data["mobile_no"] = "abcd1234"

        response = self.client.post(self.url, reservation_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("mobile_no", response.data)
