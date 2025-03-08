# Generated by Django 5.1.7 on 2025-03-07 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analyser', '0003_visitors_static_trust_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBehavior',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.CharField(max_length=255)),
                ('keystroke_latency', models.FloatField()),
                ('key_hold_time', models.FloatField()),
                ('flight_time', models.FloatField()),
                ('typing_speed', models.FloatField()),
                ('is_legitimate', models.BooleanField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
