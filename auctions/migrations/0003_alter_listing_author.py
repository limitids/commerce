# Generated by Django 4.0.2 on 2022-02-20 20:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_rename_userid_bid_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]