# Generated by Django 4.2.6 on 2024-01-05 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_reservation_series_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='series_id',
            field=models.UUIDField(blank=True, default=None, editable=False, null=True),
        ),
    ]
