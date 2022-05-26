# Generated by Django 4.0.4 on 2022-05-10 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('stars', models.IntegerField(default=0)),
                ('budget', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='HotelCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56)),
            ],
            options={
                'verbose_name_plural': 'Hotel Categories',
            },
        ),
        migrations.CreateModel(
            name='ImageResource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
        migrations.CreateModel(
            name='RoomCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56)),
            ],
            options={
                'verbose_name_plural': 'Room Categories',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_price', models.IntegerField()),
                ('selling_price', models.IntegerField()),
                ('cost_price', models.IntegerField()),
                ('discount', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='room_category', to='hotels.roomcategory')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_room_key', to='hotels.hotel')),
            ],
        ),
        migrations.CreateModel(
            name='MealPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=56)),
                ('description', models.TextField()),
                ('pricing', models.IntegerField(default=0)),
                ('configurable', models.BooleanField(default=True)),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='meal_hotel', to='hotels.hotel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='room_meal_plan', to='hotels.room')),
            ],
        ),
        migrations.CreateModel(
            name='HotelImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_image', to='hotels.hotel')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_image', to='hotels.imageresource')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='hotel_category', to='hotels.hotelcategory'),
        ),
    ]
