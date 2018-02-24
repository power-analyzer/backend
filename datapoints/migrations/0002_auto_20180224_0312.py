# Generated by Django 2.0 on 2018-02-24 03:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnarchivedMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('power', models.FloatField(null=True)),
                ('voltage', models.FloatField(null=True)),
                ('current', models.FloatField(null=True)),
                ('phase', models.FloatField(null=True)),
                ('circuit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datapoints.Circuit')),
            ],
        ),
        migrations.AlterField(
            model_name='measurement',
            name='time',
            field=models.DateTimeField(),
        ),
    ]
