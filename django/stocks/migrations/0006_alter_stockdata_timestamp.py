# Generated by Django 5.0.4 on 2024-04-29 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0005_alter_stockdata_exchange_gmtoffset'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockdata',
            name='timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]