# Generated by Django 2.1.7 on 2019-03-07 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='ip_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_rate',
        ),
        migrations.AddField(
            model_name='order',
            name='name',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[(1, 'Cформирован'), (2, 'Подтвержден'), (3, 'Оплачен'), (4, 'В процессе оплаты'), (5, 'Отгружен')], default=1),
        ),
    ]