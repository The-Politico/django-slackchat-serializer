# Generated by Django 2.1.4 on 2020-04-01 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slackchat', '0009_auto_20190219_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='api_id',
            field=models.SlugField(blank=True, editable=False, help_text='Slack API channel ID', max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='team_id',
            field=models.SlugField(blank=True, editable=False, help_text='Slack API team ID', max_length=15, null=True),
        ),
    ]
