# Generated by Django 2.0.4 on 2018-11-01 20:50

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slackchat', '0006_auto_20181101_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='serialized',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]