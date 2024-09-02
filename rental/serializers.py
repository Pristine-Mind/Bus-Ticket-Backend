from django.utils import timezone
from django.db import transaction

from rest_framework import serializers
from .models import Reservation
from .tasks import send_booking_confirmation_email


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        if data['journey_from'] == data['journey_to']:
            raise serializers.ValidationError("Journey From and Journey To cannot be the same.")

        if data['date_of_travel'] < timezone.now().date():
            raise serializers.ValidationError("Date of Travel cannot be in the past.")

        return data

    def create(self, validated_data):
        reservation = super().create(validated_data)
        email = validated_data['email']
        username = validated_data['name']
        transaction.on_commit(lambda: send_booking_confirmation_email.delay(
            email,
            username,
        ))

        return reservation
