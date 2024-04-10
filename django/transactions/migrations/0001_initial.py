# Generated by Django 5.0.3 on 2024-03-25 05:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rules', '0001_initial'),
        ('stocks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=25)),
                ('timestamp', models.DateTimeField()),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField(max_length=28)),
                ('rule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rules.rules')),
                ('ticker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stocks.stocks')),
            ],
            options={
                'indexes': [models.Index(fields=['rule'], name='transaction_rule_id_a541c8_idx')],
            },
        ),
    ]
