# Generated by Django 2.0.2 on 2018-02-07 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slackchat', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='publish_path',
            field=models.CharField(blank=True, help_text="A relative path that a renderer may use when         publishing the slackchat, e.g.,         <span style='color:grey; font-weight:bold;'>/2018-02-12/econ-chat/        </span>.", max_length=300, unique=True),
        ),
    ]