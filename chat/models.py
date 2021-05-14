from django.db import models
from authapp.models import Userreg


# Create your models here.


class Room(models.Model):
    name = models.CharField(max_length=20)


class Chat(models.Model):
    uid = models.ForeignKey(Userreg, on_delete=models.CASCADE,null=False, blank=False, related_name='Userid')
    chat = models.CharField(max_length=5000)
    roomid = models.ForeignKey(Room,on_delete=models.CASCADE,null=False, blank=False, related_name='RoomId')
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("date_created",)
