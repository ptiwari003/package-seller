# Generated by Django 4.0.4 on 2022-05-09 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Cities', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='city',
            options={'verbose_name_plural': 'city'},
        ),
        migrations.AlterModelOptions(
            name='citypair',
            options={'verbose_name_plural': 'City Pairs'},
        ),
    ]
