# Generated by Django 4.0.2 on 2022-02-20 19:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bid',
            old_name='userid',
            new_name='user',
        ),
    ]