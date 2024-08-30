from rest_framework import serializers

from .models import FeedbackReview, FAQ


class FeedbackReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackReview
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
