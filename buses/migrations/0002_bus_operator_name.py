# Generated by Django 4.0.4 on 2022-05-10 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='operator_name',
            field=models.CharField(default='', max_length=255),
        ),
    ]
