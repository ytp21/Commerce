# Generated by Django 3.2 on 2021-05-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_auctionlisting_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auctionlisting',
            name='content',
        ),
        migrations.AddField(
            model_name='auctionlisting',
            name='delete',
            field=models.BooleanField(null=True),
        ),
    ]
