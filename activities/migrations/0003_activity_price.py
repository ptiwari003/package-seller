# Generated by Django 4.0.4 on 2022-05-12 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_activity_configurable_delete_particular'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
