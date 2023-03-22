# Generated by Django 4.1.7 on 2023-03-22 09:35

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[(orders.models.CleaningOrderStatus['PLANNED'], 'planned'), (orders.models.CleaningOrderStatus['IN_PROGRESS'], 'in_progress'), (orders.models.CleaningOrderStatus['COMPLETED'], 'completed'), (orders.models.CleaningOrderStatus['CONFIRMED'], 'confirmed'), (orders.models.CleaningOrderStatus['OVERDUE'], 'overdue'), (orders.models.CleaningOrderStatus['DECLINED'], 'declined'), (orders.models.CleaningOrderStatus['OTHER'], 'other')], default=orders.models.CleaningOrderStatus['PLANNED'], max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='type',
            field=models.CharField(choices=[(orders.models.CleaningOrderType['DAILY'], 'daily'), (orders.models.CleaningOrderType['WEEKLY'], 'weekly'), (orders.models.CleaningOrderType['MONTHLY'], 'monthly'), (orders.models.CleaningOrderType['COMPLAINT'], 'complaint'), (orders.models.CleaningOrderType['OTHER'], 'other')], max_length=100),
        ),
    ]
