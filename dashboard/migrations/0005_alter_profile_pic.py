# Generated by Django 4.1.3 on 2022-11-14 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0004_alter_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
