# Generated by Django 3.0.5 on 2021-04-16 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
        ('forum', '0020_auto_20210416_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='authorpost', to='authapp.Userreg'),
        ),
    ]
