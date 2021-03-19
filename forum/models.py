from datetime import datetime

from django.db import models
from django.urls import reverse

from authapp.models import Userreg


# Create your models here.

class topic(models.Model):
    topic_title = models.CharField(max_length=120, primary_key=True)

    def __str__(self):
        return self.topic_title

    class Meta:
        db_table = "topic"


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='Userreg.id+')
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    thumbnail = models.ImageField(blank=True)
    topic_title = models.ForeignKey(topic, on_delete=models.CASCADE, related_name='topic.topic_tile+')
    Featured = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField(Userreg, related_name='Post_likes')


    def __str__(self):
        return self.title

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        self.full_clean()  # performs regular validation then clean()
        super(Post, self).save(*args, **kwargs)

    def clean(self):
        from django.utils.html import strip_tags
        if self.title:
            self.title = self.title.strip()

        if self.body:
            self.body = strip_tags(self.body)

    def get_absolute_url(self):
        return reverse('forums:Post_detail', kwargs={"pk": self.id})

    class Meta:
        db_table = "posts"
