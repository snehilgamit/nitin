# Generated by Django 5.0.6 on 2024-06-16 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Eventmanagement', '0007_temporaryaddeventdb'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventdetails',
            name='event_hotel',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
