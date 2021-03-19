from datetime import datetime

from django.db import models


# Create your models here.
class UserRoles(models.Model):
    RoleName = models.CharField(max_length=100, primary_key=True, verbose_name='RoleName')

    class Meta:
        db_table = "userrole"


class Userreg(models.Model):
    Username = models.CharField(max_length=100)
    Useremail = models.CharField(max_length=100)
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    datecreated = models.DateTimeField(default=datetime.now, blank=True)
    Role = models.ForeignKey(UserRoles, on_delete=models.CASCADE, default="User", related_name='UserRoles.RoleName+')
    user_thumbnail =models.ImageField()

    def __str__(self):
        return str(self.Username)
    class Meta:
        db_table = "useregister"


