from django.db import models
from forum.models import Userreg


# Create your models here.
class UserPost(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, default='Post')
    author = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='Userreg.id+')
    body = models.TextField()

    class Meta:
        db_table = "UserPosts"
