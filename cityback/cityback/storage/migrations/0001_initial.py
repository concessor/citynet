# Generated by Django 2.0.2 on 2018-03-05 13:56

from django.db import migrations, models
import django.db.models.deletion


# noinspection PyUnresolvedReferences,PyUnresolvedReferences
class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DublinBikesStation',
            fields=[
                ('station_number', models.IntegerField(primary_key=True, serialize=False)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('name', models.CharField(max_length=80)),
                ('address', models.CharField(max_length=120)),
                ('bonus', models.BooleanField(default=False)),
                ('contract_name', models.CharField(max_length=30)),
                ('banking', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DublinBikesStationRealTimeUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=30)),
                ('last_update', models.CharField(max_length=20)),
                ('available_bikes', models.IntegerField()),
                ('available_bike_stands', models.IntegerField()),
                ('bike_stands', models.IntegerField()),
                ('parent_station', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='storage.DublinBikesStation')),
            ],
        ),
    ]
