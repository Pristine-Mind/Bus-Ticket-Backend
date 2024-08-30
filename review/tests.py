from rest_framework.test import APITestCase
from rest_framework import status

from review.models import FeedbackReview
from review.factories import FeedbackReviewFactory, FAQFactory, UserFactory


class FeedbackReviewAPITestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.feedback_review_list_url = '/api/v1/feedback-reviews/'
        self.feedback_review_detail_url = lambda pk: f'/api/v1/feedback-reviews/{pk}/'

    def test_create_feedback_review(self):
        """Test the API to create a new feedback review."""
        data = {
            "title": "Amazing product",
            "content": "This is the best product I have ever bought!",
            "rating": 5,
            "user": self.user.id
        }
        response = self.client.post(self.feedback_review_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FeedbackReview.objects.count(), 1)
        self.assertEqual(FeedbackReview.objects.get().title, "Amazing product")

    def test_list_feedback_reviews(self):
        """Test the API to list feedback reviews."""
        FeedbackReviewFactory.create_batch(5, user=self.user)
        response = self.client.get(self.feedback_review_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 5)

    def test_feedback_review_permissions(self):
        """Test that only authenticated users can post feedback reviews."""
        self.client.logout()  # Log out the authenticated user
        data = {
            "title": "Unauthorized review",
            "content": "This should not be allowed!",
            "rating": 1,
            "user": self.user.id
        }
        response = self.client.post(self.feedback_review_list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(FeedbackReview.objects.count(), 0)


class FAQAPITestCase(APITestCase):

    def setUp(self):
        self.faq_list_url = '/api/v1/faqs/'
        self.faq_detail_url = lambda pk: f'/api/v1/faqs/{pk}/'

    def test_list_faqs(self):
        """Test the API to list FAQs."""
        FAQFactory.create_batch(3)
        response = self.client.get(self.faq_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 3)

    def test_retrieve_faq(self):
        """Test the API to retrieve a specific FAQ."""
        faq = FAQFactory()
        response = self.client.get(self.faq_detail_url(faq.pk))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], faq.question)

    def test_faq_is_readonly(self):
        """Test that the FAQ API is read-only."""
        faq = FAQFactory()
        data = {
            "question": "Can this be updated?",
            "answer": "This should not be allowed."
        }
        response = self.client.put(self.faq_detail_url(faq.pk), data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
