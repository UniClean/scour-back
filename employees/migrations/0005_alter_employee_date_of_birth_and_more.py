# Generated by Django 4.1.7 on 2023-04-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_alter_position_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='date_of_birth',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='employee',
            name='date_of_employment',
            field=models.DateTimeField(),
        ),
    ]