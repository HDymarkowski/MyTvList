# Generated by Django 2.2.17 on 2021-04-03 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyTvList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='favourite_Show_Name',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]