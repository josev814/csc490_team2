# Generated by Django 5.0.4 on 2024-04-29 14:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0007_remove_stocksearch_stocks_stoc_search__d18376_idx_and_more'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='stockdata',
            name='stocks_stoc_ticker__f939d5_idx',
        ),
        migrations.RemoveIndex(
            model_name='stocks',
            name='stocks_stoc_ticker_7e2ecb_idx',
        ),
        migrations.RemoveIndex(
            model_name='stocksearch',
            name='stocks_stoc_search__7cc4ff_idx',
        ),
    ]
