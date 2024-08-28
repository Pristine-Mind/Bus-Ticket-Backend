from django.contrib.auth.models import User
from django.db import models


class FeedbackReview(models.Model):
    """
    Model to store user feedback and reviews.

    Attributes
    ----------
    user : ForeignKey
        A reference to the user who submitted the feedback or review.
    title : CharField
        The title or subject of the feedback or review.
    content : TextField
        The main content or body of the feedback or review.
    rating : PositiveIntegerField
        The rating provided by the user, typically on a scale of 1-5.
    created_at : DateTimeField
        The date and time when the feedback or review was created.
    updated_at : DateTimeField
        The date and time when the feedback or review was last updated.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="feedback_reviews")
    title = models.CharField(max_length=200)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class FAQ(models.Model):
    """
    Model to store frequently asked questions (FAQs).

    Attributes
    ----------
    question : CharField
        The question being asked frequently.
    answer : TextField
        The answer to the frequently asked question.
    created_at : DateTimeField
        The date and time when the FAQ was created.
    updated_at : DateTimeField
        The date and time when the FAQ was last updated.
    """

    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question
