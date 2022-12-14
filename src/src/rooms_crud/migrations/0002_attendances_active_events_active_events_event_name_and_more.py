# Generated by Django 4.1.3 on 2022-11-08 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms_crud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendances',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='events',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='events',
            name='event_name',
            field=models.CharField(default='', max_length=255, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rooms',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='users',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
