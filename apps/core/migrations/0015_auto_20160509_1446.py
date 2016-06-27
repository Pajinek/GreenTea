# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def set_default_data(apps, schema_editor):
    #removed_duplicated(apps, schema_editor)
    FileLog = apps.get_model("core", "FileLog")
    for it in FileLog.objects.exclude(path=""):
        it.url = it.path
        it.is_downloaded = True
        it.save()


def unset_default_data(apps, schema_editor):
    #removed_duplicated(apps, schema_editor)
    FileLog = apps.get_model("core", "FileLog")
    for it in FileLog.objects.filter(path=""):
        it.path = it.url
        it.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_filelog_index_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='filelog',
            name='is_downloaded',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='filelog',
            name='is_indexed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='filelog',
            name='to_removed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='filelog',
            name='url',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='filelog',
            name='path',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.RunPython(set_default_data, unset_default_data),
    ]
