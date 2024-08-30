from django.core.management.base import BaseCommand
from django.utils import timezone

from user.models import User
from review.models import FeedbackReview, FAQ


class Command(BaseCommand):
    help = "Load initial data into FeedbackReview and FAQ models"

    def handle(self, *args, **kwargs):
        self.stdout.write("Creating users...")
        users = [
            {"username": "user1", "email": "user1@example.com", "password": "password1"},
            {"username": "user2", "email": "user2@example.com", "password": "password2"},
            {"username": "user3", "email": "user3@example.com", "password": "password3"},
        ]

        created_users = []
        for user_data in users:
            user, created = User.objects.get_or_create(
                username=user_data["username"], defaults={"email": user_data["email"]}
            )
            if created:
                user.set_password(user_data["password"])
                user.save()
            created_users.append(user)

        self.stdout.write("Creating FAQ entries...")
        faqs = [
            {"question": "What is the return policy?", "answer": "You can return any item within 30 days."},
            {"question": "How long does shipping take?", "answer": "Shipping typically takes 3-5 business days."},
            {"question": "Do you ship internationally?", "answer": "Yes, we ship to most countries."},
            {"question": "What payment methods do you accept?", "answer": "We accept credit/debit cards, PayPal, and more."},
            {
                "question": "How can I track my order?",
                "answer": "You can track your order using the tracking link provided in the confirmation email.",
            },
            {
                "question": "Can I change my order after placing it?",
                "answer": "You can change your order within 24 hours of placing it.",
            },
            {
                "question": "What if I receive a damaged item?",
                "answer": "Contact our support team to arrange a replacement or refund.",
            },
            {"question": "How do I create an account?", "answer": "Click on the 'Sign Up' button and fill in your details."},
            {
                "question": "Can I save items to a wishlist?",
                "answer": "Yes, you can save items to your wishlist by clicking the 'Add to Wishlist' button.",
            },
            {
                "question": "What is your privacy policy?",
                "answer": "Our privacy policy is available on our website and explains how we protect your data.",
            },
        ]

        for faq_data in faqs:
            FAQ.objects.get_or_create(
                question=faq_data["question"],
                defaults={
                    "answer": faq_data["answer"],
                    "created_at": timezone.now(),
                    "updated_at": timezone.now(),
                },
            )

        self.stdout.write("Creating FeedbackReview entries...")
        reviews = [
            {
                "user": created_users[0],
                "title": "Great service",
                "content": "I am very satisfied with the service provided.",
                "rating": 5,
            },
            {
                "user": created_users[1],
                "title": "Average experience",
                "content": "The service was okay, but could be better.",
                "rating": 3,
            },
            {
                "user": created_users[2],
                "title": "Excellent product",
                "content": "The product quality exceeded my expectations.",
                "rating": 5,
            },
            {
                "user": created_users[0],
                "title": "Fast delivery",
                "content": "I received my order earlier than expected.",
                "rating": 4,
            },
            {
                "user": created_users[1],
                "title": "Poor customer support",
                "content": "I had a hard time getting in touch with support.",
                "rating": 2,
            },
            {
                "user": created_users[2],
                "title": "Value for money",
                "content": "Good quality product for the price.",
                "rating": 4,
            },
            {
                "user": created_users[0],
                "title": "Not satisfied",
                "content": "The product did not meet my expectations.",
                "rating": 2,
            },
            {
                "user": created_users[1],
                "title": "Would buy again",
                "content": "I would definitely buy from this store again.",
                "rating": 5,
            },
            {
                "user": created_users[2],
                "title": "Great packaging",
                "content": "The product was well-packaged and arrived in perfect condition.",
                "rating": 4,
            },
            {
                "user": created_users[0],
                "title": "Slow shipping",
                "content": "Shipping took longer than expected.",
                "rating": 3,
            },
        ]

        for review_data in reviews:
            FeedbackReview.objects.get_or_create(
                user=review_data["user"],
                title=review_data["title"],
                defaults={
                    "content": review_data["content"],
                    "rating": review_data["rating"],
                    "created_at": timezone.now(),
                    "updated_at": timezone.now(),
                },
            )

        self.stdout.write(self.style.SUCCESS("Successfully loaded initial data."))
