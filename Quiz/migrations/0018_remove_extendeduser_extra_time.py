# Generated by Django 3.2.6 on 2022-01-09 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0017_extendeduser_extra_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendeduser',
            name='extra_time',
        ),
    ]
