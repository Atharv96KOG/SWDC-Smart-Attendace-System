# Generated by Django 5.1.2 on 2024-10-10 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_coordinator_profile_picture_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='currentData',
        ),
        migrations.DeleteModel(
            name='Departments',
        ),
        migrations.DeleteModel(
            name='stats',
        ),
        migrations.AlterModelOptions(
            name='activity',
            options={},
        ),
        migrations.RemoveField(
            model_name='activity',
            name='allotment_done',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='current_count',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='domain',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='enabled',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='flagship_event',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='max_count',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='message',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='only_females',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='only_males',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='report_filling',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='report_verification',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='t_and_c',
        ),
        migrations.AddField(
            model_name='activity',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='latitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='longitude',
            field=models.FloatField(null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='map_link',
            field=models.URLField(blank=True, max_length=2000, null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='time',
            field=models.TimeField(null=True),
        ),
        migrations.AlterField(
            model_name='activity',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]
