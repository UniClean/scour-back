# Generated by Django 4.1.7 on 2023-03-12 18:06

from django.db import migrations, models
import orders.models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_report_deadline_order_start_when'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('PLANNED', 'planned'), ('IN_PROGRESS', 'in_progress'), ('COMPLETED', 'completed'), ('CONFIRMED', 'confirmed'), ('OVERDUE', 'overdue'), ('DECLINED', 'declined'), ('OTHER', 'other')], default=orders.models.CleaningOrderStatus['PLANNED'], max_length=100),
        ),
    ]
