# Generated by Django 4.1.3 on 2022-11-14 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_profile_balance_delete_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='pic',
            field=models.ImageField(blank=True, default='profile_pics/default_profile_pic.jpg', null=True, upload_to='profile_pics'),
        ),
    ]
