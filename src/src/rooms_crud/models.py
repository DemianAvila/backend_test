from django.db import models

# Create your models here.
class Users(models.Model):
    user_name = models.CharField(max_length=255, unique=True)
    user_type = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)

class Rooms(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    room_capacity = models.IntegerField()

class Events(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=255)
    starts = models.DateTimeField()
    ends = models.DateTimeField()

class Attendances(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)

