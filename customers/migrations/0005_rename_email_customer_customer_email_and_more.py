# Generated by Django 4.1.7 on 2023-03-22 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_customer_email_customer_customer_website_customer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='email_customer',
            new_name='email',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='website_customer',
            new_name='website',
        ),
    ]
