# Generated by Django 3.0.7 on 2021-04-03 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareKey',
            fields=[
                ('location', models.TextField()),
                ('token', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('expiration_seconds', models.BigIntegerField()),
            ],
        ),
    ]
