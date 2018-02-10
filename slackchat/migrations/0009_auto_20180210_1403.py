# Generated by Django 2.0.2 on 2018-02-10 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slackchat', '0008_auto_20180210_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='service_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='thumb_height',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='thumb_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='thumb_width',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='video_html',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='video_html_height',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='attachment',
            name='video_html_width',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]