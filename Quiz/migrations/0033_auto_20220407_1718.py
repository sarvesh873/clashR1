# Generated by Django 3.2.6 on 2022-04-07 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0032_auto_20220407_1706'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extendeduser',
            name='extra_tab',
        ),
        migrations.AlterField(
            model_name='extendeduser',
            name='tab',
            field=models.IntegerField(default=3),
        ),
    ]