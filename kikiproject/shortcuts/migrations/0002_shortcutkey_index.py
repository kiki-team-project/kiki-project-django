# Generated by Django 4.2.9 on 2024-01-30 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcuts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shortcutkey',
            name='index',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
