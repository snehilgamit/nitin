# Generated by Django 5.0.3 on 2024-03-30 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Eventmanagement', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='outofficeproduct',
            old_name='unique_identifier',
            new_name='event_id',
        ),
    ]
