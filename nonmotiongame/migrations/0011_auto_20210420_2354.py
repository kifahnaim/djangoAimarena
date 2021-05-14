# Generated by Django 3.0.5 on 2021-04-20 23:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nonmotiongame', '0010_auto_20210420_2335'),
    ]

    operations = [
        migrations.AddField(
            model_name='rank',
            name='score_max',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rank',
            name='score_min',
            field=models.FloatField(default=1000),
            preserve_default=False,
        ),
    ]
