# Generated by Django 4.2.15 on 2024-08-31 00:37

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Enter your full name.', max_length=100, verbose_name='Full Name')),
                ('mobile_no', phonenumber_field.modelfields.PhoneNumberField(help_text='Enter your mobile number.', max_length=128, region='NP', verbose_name='Mobile Number')),
                ('date_of_travel', models.DateField(help_text='Select the date of your travel.', verbose_name='Date of Travel')),
                ('duration_type', models.CharField(choices=[('day_based', 'Day Based'), ('hourly_based', 'Hourly Based')], help_text='Select whether the duration is day-based or hourly-based.', max_length=12, verbose_name='Duration Type')),
                ('passenger_numbers', models.PositiveIntegerField(help_text='Enter the number of passengers.', verbose_name='Number of Passengers')),
                ('journey_from', models.CharField(choices=[('kathmandu', 'Kathmandu'), ('pokhara', 'Pokhara'), ('lalitpur', 'Lalitpur'), ('bhaktapur', 'Bhaktapur'), ('biratnagar', 'Biratnagar'), ('birgunj', 'Birgunj'), ('dharan', 'Dharan'), ('bharatpur', 'Bharatpur'), ('butwal', 'Butwal'), ('hetauda', 'Hetauda'), ('janakpur', 'Janakpur'), ('dhangadhi', 'Dhangadhi'), ('nepalgunj', 'Nepalgunj'), ('itahari', 'Itahari'), ('tulsipur', 'Tulsipur'), ('siddharthanagar', 'Siddharthanagar (Bhairahawa)'), ('ghorahi', 'Ghorahi'), ('damak', 'Damak'), ('rajbiraj', 'Rajbiraj'), ('lahan', 'Lahan'), ('inaruwa', 'Inaruwa'), ('tikapur', 'Tikapur'), ('kirtipur', 'Kirtipur'), ('bhadrapur', 'Bhadrapur'), ('mechinagar', 'Mechinagar (Kakarbhitta)')], help_text='Select the starting location of your journey.', max_length=100, verbose_name='Journey From')),
                ('journey_to', models.CharField(choices=[('kathmandu', 'Kathmandu'), ('pokhara', 'Pokhara'), ('lalitpur', 'Lalitpur'), ('bhaktapur', 'Bhaktapur'), ('biratnagar', 'Biratnagar'), ('birgunj', 'Birgunj'), ('dharan', 'Dharan'), ('bharatpur', 'Bharatpur'), ('butwal', 'Butwal'), ('hetauda', 'Hetauda'), ('janakpur', 'Janakpur'), ('dhangadhi', 'Dhangadhi'), ('nepalgunj', 'Nepalgunj'), ('itahari', 'Itahari'), ('tulsipur', 'Tulsipur'), ('siddharthanagar', 'Siddharthanagar (Bhairahawa)'), ('ghorahi', 'Ghorahi'), ('damak', 'Damak'), ('rajbiraj', 'Rajbiraj'), ('lahan', 'Lahan'), ('inaruwa', 'Inaruwa'), ('tikapur', 'Tikapur'), ('kirtipur', 'Kirtipur'), ('bhadrapur', 'Bhadrapur'), ('mechinagar', 'Mechinagar (Kakarbhitta)')], help_text='Select the destination of your journey.', max_length=100, verbose_name='Journey To')),
                ('vehicle_type', models.CharField(choices=[('bus', 'Bus'), ('minivan', 'Minivan'), ('car', 'Car')], help_text='Select the type of vehicle for your journey.', max_length=20, verbose_name='Vehicle Type')),
                ('comment', models.TextField(blank=True, help_text='Enter any additional specifications or requests (optional).', null=True, verbose_name='Additional Comments')),
            ],
        ),
    ]
