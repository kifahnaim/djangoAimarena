from django.db import models
from authapp.models import Userreg


class Rank(models.Model):
    Rank_Name = models.CharField(max_length=150)
    Rank_description = models.CharField(max_length=250)
    Rank_image = models.ImageField()
    score_min = models.FloatField()
    score_max = models.FloatField()


# Create your models here.
class User_Info(models.Model):
    Score_Avg = models.FloatField()
    Accuracy_Avg = models.FloatField()
    Hits_Avg = models.FloatField()
    Shots_Avg = models.FloatField()
    User_ID = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='UserI')
    forumpoints = models.CharField(max_length=150)


class Game_Mode(models.Model):
    Mode_Description = models.CharField(max_length=200)


class Game(models.Model):
    Start_Date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    End_Date = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    Game_Mode_ID = models.ForeignKey(Game_Mode, on_delete=models.CASCADE, related_name='Game_Mode')
    User_ID = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='UserG')


class Game_Statistics(models.Model):
    Date = models.DateTimeField(auto_now_add=True)
    Game_ID = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='Game')
    Shot = models.CharField(max_length=200)
    Hit = models.CharField(max_length=200)
    Score = models.PositiveIntegerField(default=0)
    Accuracy = models.FloatField(default=0)


class GameMode_User(models.Model):
    Game_Mode_ID = models.ForeignKey(Game_Mode, on_delete=models.CASCADE, related_name='Game_Mode_user')
    User_ID = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='User_Mode_user')
    Score_Avg = models.FloatField()
    Accuracy_Avg = models.FloatField()
    Hits_Avg = models.FloatField()
    Shots_Avg = models.FloatField()
    Rank = models.ForeignKey(Rank, null=True, blank=True, on_delete=models.CASCADE, related_name='rankuser')

class products(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    product_desc = models.CharField(max_length=200)
    product_type = models.CharField(max_length=200)
    product_image = models.ImageField(null=False)
    product_spriteimage = models.ImageField(null=True)
    is_deleted = models.BooleanField(null=True)

    class Meta:
        db_table = "products"


class userproducts(models.Model):
    product = models.ForeignKey(products, on_delete=models.CASCADE, related_name='product')
    user = models.ForeignKey(Userreg, on_delete=models.CASCADE, related_name='userproducts')

    class Meta:
        db_table = "userproducts"
