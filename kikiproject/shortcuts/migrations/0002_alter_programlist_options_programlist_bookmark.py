# Generated by Django 5.0.1 on 2024-03-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shortcuts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='programlist',
            options={'ordering': ['-bookmark']},
        ),
        migrations.AddField(
            model_name='programlist',
            name='bookmark',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]