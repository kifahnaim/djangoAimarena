from datetime import datetime

from django.contrib.auth import user_logged_in
from django.contrib.sessions.models import Session
from django.db import models

# Create your models here.
from django.utils.text import capfirst
from passlib.handlers.pbkdf2 import pbkdf2_sha256


class UserRoles(models.Model):
    RoleName = models.CharField(max_length=100, verbose_name='RoleName')

    def _str_(self):
        return str(self.RoleName)

    class Meta:
        db_table = "userrole"


class Userreg(models.Model):
    Username = models.CharField(max_length=100)
    Useremail = models.CharField(max_length=100)
    Firstname = models.CharField(max_length=100)
    Lastname = models.CharField(max_length=100)
    password = models.CharField(max_length=250)
    datecreated = models.DateTimeField(auto_now_add=True, blank=True)
    Role = models.ForeignKey(UserRoles, on_delete=models.CASCADE, default=1, related_name='userrole')
    is_active = models.BooleanField(default=False)
    user_thumbnail = models.ImageField(blank=True, upload_to='images/', default='default.jpg')

    def _str_(self):
        return str(self.Username)

    def verify_password(self, raw_password):
        return pbkdf2_sha256.verify(raw_password, self.password)

    def save(self, *args, **kwargs):
        self.full_clean()  # performs regular validation then clean()
        super(Userreg, self).save(*args, **kwargs)

    def clean(self):

        if self.Username:
            self.Username = self.Username.strip()

        if self.Firstname:
            self.Firstname = self.Firstname.strip()

        if self.Lastname:
            self.Lastname = self.Lastname.strip()

        if self.Useremail:
            self.Useremail = self.Useremail.strip()

        if self.password:
            self.password = self.password.strip()

    class Meta:
        db_table = "useregister"


class login_details(models.Model):
    user_id = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='userid')
    lastlogin = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "login_details"


class Pages(models.Model):
    permission_name = models.CharField(max_length=100, null=True)
    permission_description = models.CharField(max_length=100)

    class Meta:
        db_table = "Pages"


class Role_permissions(models.Model):
    Role_id = models.ForeignKey(UserRoles, on_delete=models.CASCADE, related_name='Role_id')
    permission_id = models.ForeignKey(Pages, on_delete=models.CASCADE, related_name='permission_id')
    ban = models.BooleanField(null=True, default=False)
    kick = models.BooleanField(null=True, default=False)
    manage_posts = models.BooleanField(null=True, default=False)
    textwelcome = models.BooleanField(null=True, default=False)
    email = models.BooleanField(null=True, default=False)
    can_access = models.BooleanField(null=True, default=False)
    can_view = models.BooleanField(null=True, default=False)
    can_promote = models.BooleanField(null=True, default=False)

    def _str_(self):
        return str(self.permission_id)

    class Meta:
        db_table = "Role_permissions"


class admin_actions(models.Model):
    user_id = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_id_actions')
    user_kick_forum = models.BooleanField(default=0)
    user_ban_forum = models.BooleanField(default=0)
    user_ban_game = models.BooleanField(default=0)
    create_appeal = models.BooleanField(default=0)

    def _str_(self):
        return str(self.user_id)

    class Meta:
        db_table = "admin_actions"


class Banfromforum(models.Model):
    Banned_until = models.DateTimeField()
    Banned_time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_id_ban')
    banned_by = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='userbanforumby')

    class Meta:
        db_table = "Banfromforum"


class kickedfromwebsite(models.Model):
    kicked_time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_id_kick')
    kicked_by = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='userkick')

    class Meta:
        db_table = "kickedfromwebsite"


class Banfromgame(models.Model):
    Banned_until = models.DateTimeField()
    Banned_time = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_id_bangame')
    banned_by = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='userbangameby')

    class Meta:
        db_table = "Banfromgame"


class UserSession(models.Model):
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='user_id_session')
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

    def user_logged_in_handler(request, customuser, **kwargs):
        if not request.session.session_key:
            request.session.save()
        session_id = request.session.session_key
        UserSession.objects.get_or_create(user=customuser, session_id=session_id)

    user_logged_in.connect(user_logged_in_handler)