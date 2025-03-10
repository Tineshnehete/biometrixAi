# Generated by Django 5.1.7 on 2025-03-07 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitorID', models.CharField(max_length=100)),
                ('fingerprint', models.CharField(max_length=100)),
                ('last_visit', models.DateTimeField()),
                ('first_visit', models.DateTimeField()),
                ('visits', models.IntegerField(default=1)),
            ],
        ),
    ]
