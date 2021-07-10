# Generated by Django 3.2 on 2021-05-29 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_comment_comment_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='creator',
            new_name='commenter',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='bidder',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='listing_bidder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='watcher',
            field=models.ManyToManyField(blank=True, null=True, related_name='listing_watcher', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='auctionlisting',
            name='creator',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='listing_creator', to=settings.AUTH_USER_MODEL),
        ),
    ]