# Generated by Django 2.0 on 2018-03-03 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datapoints', '0002_auto_20180224_0312'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuit',
            name='circuit_transformer_type',
            field=models.CharField(choices=[('10A', '10 Amp Current Transformer')], default='10A', max_length=200),
        ),
        migrations.AddField(
            model_name='circuit',
            name='pannel_side',
            field=models.CharField(choices=[('left', 'Left Side'), ('right', 'Right Side')], default='right', max_length=200),
        ),
        migrations.AddField(
            model_name='device',
            name='phase_offset',
            field=models.CharField(choices=[('left', 'Left +90'), ('right', 'Right -90')], default='right', max_length=30),
        ),
    ]
