from django.db import models

# Create your models here.
from authapp.models import Userreg


class emailnews(models.Model):
    userid = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='usernewsid')
    email = models.CharField(max_length=250)
    subscription = models.BooleanField(default=1)

    class Meta:
        db_table = "emailnews"


class newsbanner(models.Model):
    news = models.CharField(max_length=250)
    updated_by = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='usernewsupdate')
    datetime = models.DateTimeField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(null=True)

class unsubscribefeedback(models.Model):
    emailnewid = models.ForeignKey(emailnews, on_delete=models.CASCADE, related_name='emailnewsid')
    feedbackname = models.CharField(max_length=250)
    message = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        db_table = "unsubscribefeedback"


