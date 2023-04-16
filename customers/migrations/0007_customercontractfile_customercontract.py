# Generated by Django 4.1.7 on 2023-04-16 05:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0006_customer_phone_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerContractFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_file', models.FileField(upload_to='customer_contract_files')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('deleted', models.BooleanField(default=False)),
                ('deleted_date', models.DateTimeField(blank=True, null=True)),
                ('contracts', models.ManyToManyField(blank=True, to='customers.customercontractfile')),
                ('customer_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer')),
            ],
        ),
    ]