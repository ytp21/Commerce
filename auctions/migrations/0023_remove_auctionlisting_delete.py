# Generated by Django 3.2 on 2021-07-07 04:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_auctionlisting_deactivate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='delete',
        ),
    ]