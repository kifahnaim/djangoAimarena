# Generated by Django 3.0.5 on 2021-04-20 23:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nonmotiongame', '0009_auto_20210420_2334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='Rank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rankuser', to='nonmotiongame.Rank'),
        ),
    ]
