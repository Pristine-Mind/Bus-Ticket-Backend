import factory

from review.models import FeedbackReview, FAQ
from bus.factories import UserFactory


class FeedbackReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeedbackReview

    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence', nb_words=4)
    content = factory.Faker('paragraph', nb_sentences=3)
    rating = factory.Iterator([1, 2, 3, 4, 5])


class FAQFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FAQ

    question = factory.Faker('sentence', nb_words=6)
    answer = factory.Faker('paragraph', nb_sentences=5)
