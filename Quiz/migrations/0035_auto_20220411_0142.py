# Generated by Django 3.2.6 on 2022-04-10 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0034_auto_20220411_0136'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendeduser',
            name='visitedInst',
        ),
        migrations.RemoveField(
            model_name='extendeduser',
            name='visitedQue',
        ),
    ]
