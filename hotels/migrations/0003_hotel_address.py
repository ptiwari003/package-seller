# Generated by Django 4.0.4 on 2022-05-11 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotels', '0002_remove_imageresource_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotel',
            name='address',
            field=models.CharField(default='* Mandatory', max_length=255),
        ),
    ]
