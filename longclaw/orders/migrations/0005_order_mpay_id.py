# Generated by Django 2.1.7 on 2019-03-12 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20190307_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mpay_id',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]