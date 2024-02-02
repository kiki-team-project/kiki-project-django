# Generated by Django 5.0.1 on 2024-02-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_user_key_searcher_alter_user_pro_searcher'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeySearcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProSearcher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='key_searcher',
        ),
        migrations.RemoveField(
            model_name='user',
            name='pro_searcher',
        ),
        migrations.AddField(
            model_name='user',
            name='key_searcher',
            field=models.ManyToManyField(blank=True, related_name='keysearchs', to='accounts.keysearcher'),
        ),
        migrations.AddField(
            model_name='user',
            name='pro_searcher',
            field=models.ManyToManyField(blank=True, related_name='prosearchs', to='accounts.prosearcher'),
        ),
    ]
