# Generated by Django 3.2 on 2021-05-28 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0015_auto_20210528_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment_title',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
