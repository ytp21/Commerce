# Generated by Django 3.2 on 2021-06-02 02:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_auto_20210601_1728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlisting',
            name='bidder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='listing_bidder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='listing_creator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='watcher',
            field=models.ManyToManyField(blank=True, related_name='listing_watcher', to=settings.AUTH_USER_MODEL),
        ),
    ]
