# Generated by Django 2.2.17 on 2021-04-04 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyTvList', '0002_userprofile_favourite_show_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='website',
        ),
    ]