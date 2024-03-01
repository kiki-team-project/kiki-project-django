# Generated by Django 5.0.1 on 2024-03-01 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='bookmark_program',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bookmark_shortcut',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.ImageField(default='user_photos/default.png', upload_to='user_photos/'),
        ),
    ]
