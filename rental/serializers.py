from django.utils import timezone

from rest_framework import serializers
from .models import Reservation


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
