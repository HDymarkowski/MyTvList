# Generated by Django 2.2.17 on 2021-04-05 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyTvList', '0005_auto_20210405_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='favouriteShow',
            field=models.IntegerField(default=None, unique=True),
        ),
    ]