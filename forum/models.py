from datetime import datetime, timedelta

from django.db import models
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.urls import reverse

from authapp.models import Userreg
from ckeditor.fields import RichTextField


# Create your models here.

class topic(models.Model):
    topic_title = models.CharField(max_length=120)
    topic_description = models.CharField(max_length=200)
    is_visible = models.BooleanField()
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.topic_title

    def save(self, *args, **kwargs):
        self.full_clean()  # performs regular validation then clean()
        super(topic, self).save(*args, **kwargs)

    class Meta:
        db_table = "topic"


class subtopic(models.Model):
    sub_topic_title = models.CharField(max_length=120)
    sub_topic_description = models.CharField(max_length=200)
    topic = models.ForeignKey(topic, on_delete=models.CASCADE, related_name='topic_subtopic')
    slug = models.SlugField(
        verbose_name="Slug",
        allow_unicode=True,
        unique=True,
        blank=True,
        null=True)
    is_visible = models.BooleanField()
    pinned_visible = models.BooleanField()
    accepted_visible = models.BooleanField()
    rejected_visible = models.BooleanField()
    acceptedappeal_visible = models.BooleanField()
    rejectedappeal_visible = models.BooleanField()
    subtopic_visible = models.BooleanField()
    subtopic_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.topic

    def save(self, *args, **kwargs):
        if not self.slug: self.slug = slugify("AimArena" + str(datetime.now()) + self.sub_topic_title[0:3])
        super(subtopic, self).save(*args, **kwargs)

    def __str__(self):
        return self.sub_topic_title

    class Meta:
        db_table = "subtopic"


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=255, blank=True)
    author = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='authorpost')
    body = RichTextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(blank=True, null=True)
    topic_title = models.ForeignKey(subtopic, on_delete=models.CASCADE, related_name='topic_title_post')
    Featured = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField(Userreg, related_name='Post_likes')
    is_available = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    post_views = models.IntegerField(default=0,null=True,blank=True)
    appeal_accepted = models.BooleanField(default=False)
    appeal_rejected = models.BooleanField(default=False)
    is_closed = models.BooleanField(null=True, default=False)
    slug = models.SlugField(
        verbose_name="Slug",
        allow_unicode=True,
        unique=True,
        blank=True,
        null=True)

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
            self.body = self.body

    def get_absolute_url(self):
        return reverse('forums:Post_detail', kwargs={"pk": self.id})

    class Meta:
        db_table = "posts"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Post')
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='replies')
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user')
    deleted = models.BooleanField(default=False)

    def total_comments(self):
        return self.post.count()

    class Meta:
        db_table = "Comment"


class Notification(models.Model):
    Notification_Types = (
        (1, 'Like'),
        (2, 'Comment'),
        (3, 'Reply')
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='noti_post')
    sender = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='noti_from_user')
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='noti_to_user')
    Notification_type = models.IntegerField(choices=Notification_Types)
    text_preview = models.CharField(max_length=50, blank=True)
    is_read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.text_preview)

    class Meta:
        ordering = ['-date']


class Emaillogs(models.Model):
    email_type = models.CharField(max_length=200)
    email_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_email')
    email_message = models.CharField(max_length=200, null=True)
    email_token = models.CharField(max_length=200, null=True)
    email_url = models.CharField(max_length=200, null=True)

    class Meta:
        db_table = "Emaillogs"


class subtopiclatestposts(models.Model):
    subtopicnew = models.ForeignKey(subtopic, on_delete=models.CASCADE, related_name='subtopiclatest')
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_latest')
    is_read = models.BooleanField()
