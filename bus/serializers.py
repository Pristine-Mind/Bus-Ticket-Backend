from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import Bus, Route, BusRoute, Booking, BookingDetail


class BusSerializer(serializers.ModelSerializer):
    """
    Serializer for the Bus model.
    """

    class Meta:
        model = Bus
        fields = ['id', 'bus_number,', 'bus_type', 'capacity', 'availability_status']
        extra_kwargs = {
            'bus_number': {'help_text': _("Unique identifier for the bus (e.g., ABC123).")},
            'bus_type': {'help_text': _("Type of the bus (e.g., Air Conditioned, Sleeper).")},
            'capacity': {'help_text': _("Total number of seats available on the bus.")},
            'availability_status': {'help_text': _("Indicates whether the bus is available for booking.")}
        }


class RouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the Route model.
    """

    class Meta:
        model = Route
        fields = ['id', 'start_location', 'end_location', 'stops', 'scheduled_time']
        extra_kwargs = {
            'start_location': {'help_text': _("Starting point of the bus route.")},
            'end_location': {'help_text': _("Ending point of the bus route.")},
            'stops': {'help_text': _("Comma separated list of intermediate stops.")},
            'scheduled_time': {'help_text': _("Scheduled departure time of the bus.")}
        }


class BusRouteSerializer(serializers.ModelSerializer):
    """
    Serializer for the BusRoute model.
    """

    bus = BusSerializer()
    route = RouteSerializer()

    class Meta:
        model = BusRoute
        fields = ['id', 'bus', 'route', 'date', 'available_seats']
        extra_kwargs = {
            'date': {'help_text': _("Date on which the bus is scheduled for this route.")},
            'available_seats': {'help_text': _("Number of seats available for booking on this bus.")}
        }


class BookingDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the BookingDetail model.
    """

    bus_route = BusRouteSerializer()

    class Meta:
        model = BookingDetail
        fields = ['id', 'bus_route', 'seat_numbers']
        extra_kwargs = {
            'seat_numbers': {'help_text': _("The list of seat numbers assigned to the user for this route.")}
        }


class BookingSerializer(serializers.ModelSerializer):
    """
    Serializer for the Booking model.
    """

    book = BookingDetailSerializer(many=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'booking_time', 'book']
        extra_kwargs = {
            'booking_time': {'help_text': _("Time when the booking was made.")}
        }

    def create(self, validated_data):
        """
        Override the create method to handle nested BookingDetail data.
        """
        booking_details_data = validated_data.pop('book')
        booking = Booking.objects.create(**validated_data)

        for detail_data in booking_details_data:
            BusRoute = detail_data.pop('bus_route')
            booking_detail = BookingDetail.objects.create(
                booking=booking,
                bus_route=BusRoute,
                **detail_data
            )
            booking.book.add(booking_detail)

        return booking
