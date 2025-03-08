from django.db import models
from uuid import uuid5
from django.utils import timezone
# Create your models here.

# model to store user fingerprint and ip and visits
class Visitors(models.Model):
    visitorID = models.CharField(max_length=100)
    fingerprint = models.CharField(max_length=100)
    last_visit = models.DateTimeField(auto_now=True)
    first_visit = models.DateTimeField(default=timezone.now)
    visits = models.IntegerField(default=1)
    static_trust_score = models.IntegerField(default=50 )


class UserBehavior(models.Model):
    user_id = models.CharField(max_length=255)
    keystroke_latency = models.FloatField()
    key_hold_time = models.FloatField()
    flight_time = models.FloatField()
    typing_speed = models.FloatField()
    is_legitimate = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

class MouseBehavior(models.Model):

    user_id=models.CharField(max_length=255)
    mouse_speed=models.FloatField()
    mouse_acceleration=models.FloatField()
    click_variance=models.FloatField()
    is_legitimate=models.BooleanField()
    timestamp= models.DateTimeField(auto_now_add=True)




    