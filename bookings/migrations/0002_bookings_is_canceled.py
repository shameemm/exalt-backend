# Generated by Django 4.1.5 on 2023-04-26 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookings',
            name='is_canceled',
            field=models.BooleanField(default=True),
        ),
    ]
