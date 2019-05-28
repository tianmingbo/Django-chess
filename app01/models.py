from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class UserInfo(AbstractUser):
    """
        用户信息表
    """
    nid = models.AutoField(primary_key=True)
    avatar = models.FileField(upload_to="avatars/", default="avatars/default.png", verbose_name="头像")
    total = models.IntegerField(default=0)  # 总计
    victory = models.IntegerField(default=0)  # 胜场
    draw = models.IntegerField(default=0)  # 平场
    defeat = models.IntegerField(default=0)  # 负场
    score = models.IntegerField(default=1000)  # 积分
    def __str__(self):
        return self.username

