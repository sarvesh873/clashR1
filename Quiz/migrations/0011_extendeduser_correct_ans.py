# Generated by Django 3.2.6 on 2021-12-30 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0010_extendeduser_time_rz_counter'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='correct_ans',
            field=models.ImageField(default=0, upload_to=''),
        ),
    ]
