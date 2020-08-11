# Generated by Django 3.0.8 on 2020-07-31 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auction_bid_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='category',
            field=models.CharField(default='others', max_length=64),
        ),
        migrations.AddField(
            model_name='auction',
            name='url',
            field=models.CharField(default='', max_length=64),
        ),
        migrations.AlterField(
            model_name='auction',
            name='bid',
            field=models.IntegerField(default=0),
        ),
    ]