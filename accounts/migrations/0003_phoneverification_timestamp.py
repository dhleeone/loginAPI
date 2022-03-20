# Generated by Django 4.0.3 on 2022-03-19 04:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneverification',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]