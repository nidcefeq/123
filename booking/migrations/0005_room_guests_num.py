# Generated by Django 4.2.19 on 2025-02-13 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_room'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='guests_num',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
