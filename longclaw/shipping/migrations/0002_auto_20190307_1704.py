# Generated by Django 2.1.7 on 2019-03-07 14:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shipping', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='address',
            name='country',
        ),
        migrations.RemoveField(
            model_name='address',
            name='line_1',
        ),
        migrations.RemoveField(
            model_name='address',
            name='line_2',
        ),
        migrations.RemoveField(
            model_name='address',
            name='postcode',
        ),
    ]
