# Generated by Django 5.0.2 on 2024-03-01 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(db_index=True, max_length=254, unique=True),
        ),
    ]
