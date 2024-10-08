# Generated by Django 4.2.15 on 2024-08-28 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bus", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="book",
            field=models.ManyToManyField(
                help_text="Multiple bookings for different routes.", to="bus.bookingdetail", verbose_name="Book"
            ),
        ),
    ]
