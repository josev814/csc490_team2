# Generated by Django 5.0.3 on 2024-04-08 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stocks',
            name='stock_type',
            field=models.CharField(max_length=25),
        ),
    ]
