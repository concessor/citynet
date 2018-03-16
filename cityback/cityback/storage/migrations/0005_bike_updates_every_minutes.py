# Generated by Django 2.0.2 on 2018-03-16 11:33
from itertools import islice

import numpy as np
import datetime
from django.db import migrations, models
from django.db.models import Min, Max

from cityback.storage.apps import getBikesTimeRange, roundTime
import time


def migrate_every_minutes(apps, schema_editor):

    MyModel = apps.get_model('storage', 'dublinbikesstationrealtimeupdate')

    time_delta = 60
    times = MyModel.objects.all().aggregate(
        Min('station_last_update'), Max('station_last_update'))
    startTime = times['station_last_update__min']
    lastTime = times['station_last_update__max']
    start, end = roundTime(startTime, time_delta), roundTime(lastTime, time_delta)

    num_dates = (end - start) // datetime.timedelta(seconds=time_delta) + 1
    date_list = [start + datetime.timedelta(seconds=(time_delta * x))
                 for x in range(num_dates)]

    assert(date_list[-1] == end)
    print("number of times", num_dates)

    time_delta = 60
    stopwatch_start = time.time()
    list_stations = MyModel.objects.all().distinct('parent_station')
    list_stations = [l.parent_station for l in list_stations]
    list_stations_pk = [l.station_number for l in list_stations]
    num_stations = len(list_stations)

    all = MyModel.objects.all()
    count = all.count()
    print("number of update records", count)
    if(count == 0):
        return

    vlqs = all.values_list('station_last_update',
                           'available_bikes',
                           'bike_stands',
                           'parent_station',
                           'timestamp', 'available_bike_stands', 'status')
    r = np.core.records.fromrecords(vlqs, names=[
        'station_last_update', 'available_bikes', 'bike_stands',
        'parent_station', 'timestamp', 'available_bike_stands', 'status'])

    print("all data dumped in r")
    matrix = np.zeros((num_dates, num_stations, 5), dtype=object)

    print("filling numpy array")
    for i, data in enumerate(r):
        if i % 10000 == 0:
            print(i)

        rounded_time = roundTime(data[0], time_delta)
        try:
            idx = date_list.index(rounded_time)
            station_idx = list_stations_pk.index(data[3])
        except ValueError:
            print("Error!, unable to find roundedtime = {} or stationidx="
                  "".format(rounded_time, data[3]))
            continue

        matrix[idx, station_idx] = np.array(list(data))[[0, 1, 2, 5, 6]]

    empty = matrix[:, :, 0] == 0

    print("filling holes")
    # find first data
    for sidx in range(num_stations):
        idx = 0
        while empty[idx, sidx]:
            idx += 1
        # fill the begining
        matrix[0:idx, sidx] = matrix[idx, sidx]

    for sidx in range(num_stations):
        fill = matrix[0, sidx]

        for i in range(matrix.shape[0]):
            if empty[i, sidx]:
                matrix[i, sidx] = fill
            else:
                fill = matrix[i, sidx]
    end = time.time()
    print("filled in {}s".format(
        end - stopwatch_start
    ))

    print("Filling db")
    objects = []
    for sidx in range(num_stations):
        if sidx % 5 == 0:
            print(sidx)
        for i in range(matrix.shape[0]):
            objects.append(MyModel(
                parent_station=list_stations[sidx],
                timestamp=date_list[i].replace(
                    tzinfo=datetime.timezone.utc),
                status=matrix[i, sidx, 4],
                station_last_update=matrix[i, sidx, 0],
                available_bikes=matrix[i, sidx, 1],
                available_bike_stands=matrix[i, sidx, 3],
                bike_stands=matrix[i, sidx, 2],
            ))
    MyModel.objects.all().delete()
    batch_size = 1000
    MyModel.objects.bulk_create(objects, batch_size)


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0004_db_refactoring'),
    ]

    operations = [
        migrations.AddField(
            model_name='dublinbikesstationrealtimeupdate',
            name='timestamp',
            field=models.DateTimeField(null=True),
        ),
        migrations.RenameField(
            model_name='dublinbikesstationrealtimeupdate',
            old_name='last_update',
            new_name='station_last_update',
        ),
        migrations.RunPython(migrate_every_minutes),
    ]
