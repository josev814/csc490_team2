# Generated by Django 5.0.2 on 2024-03-01 21:29

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_users_created_alter_users_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]