# Generated by Django 3.2.6 on 2021-12-03 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0009_extendeduser_red_zone_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='time_rz_counter',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
