from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import FeedbackReview, FAQ
from .serializers import FeedbackReviewSerializer, FAQSerializer


class FeedbackReviewViewSet(viewsets.ModelViewSet):
    queryset = FeedbackReview.objects.all()
    serializer_class = FeedbackReviewSerializer

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = []
        return super().get_permissions()

    def update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PUT' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        return Response({"detail": "Method 'PATCH' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def destroy(self, request, *args, **kwargs):
        return Response({"detail": "Method 'DELETE' not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
