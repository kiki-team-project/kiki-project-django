# Generated by Django 5.0.1 on 2024-03-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_bookmark_program_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='os_type',
            field=models.CharField(choices=[('window', '윈도우'), ('mac', '맥')], default='windows', max_length=15),
        ),
    ]