# Generated by Django 3.2.6 on 2022-01-04 04:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0015_extendeduser_prev_que_correct'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extendeduser',
            old_name='num_of_RZs',
            new_name='num_of_lifeline',
        ),
    ]
