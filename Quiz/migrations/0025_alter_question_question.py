# Generated by Django 3.2.6 on 2022-02-28 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0024_extendeduser_login_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question',
            field=models.TextField(max_length=500),
        ),
    ]