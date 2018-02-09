# Generated by Django 2.0 on 2018-02-09 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='Circuit',
        ),
        migrations.AddField(
            model_name='circuit',
            name='relative_id',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='circuit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='datapoints.Circuit'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='current',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='phase',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='measurement',
            name='voltage',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
