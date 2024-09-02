from celery import shared_task

from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_booking_confirmation_email(user_email, user_first_name):
    subject = 'Booking Confirmation'
    message = (
        f"Hello {user_first_name},\n\n"
        "Your booking is under process and our team will contact you soon.\n\n"
        "Thank you for choosing our service!"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
