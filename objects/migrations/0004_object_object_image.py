# Generated by Django 4.1.7 on 2023-04-16 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('objects', '0003_requiredobjectinventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='object',
            name='object_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/objects/'),
        ),
    ]