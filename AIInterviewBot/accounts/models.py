from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from contents.models import DashBoard

User = settings.AUTH_USER_MODEL

class UserProfile(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/',blank=True, null=True)
    GENDER_CHOICES = (
        ('M', '男性'),
        ('F', '女性'),
        ('O', '其他'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    birth_date = models.DateField(blank=True,null=True)
    DEGREE_CHOICES = (
        ('S', '高中'),
        ('B', '學士'),
        ('M', '碩士'),
        ('D', '博士'),
    )
    degree = models.CharField(max_length=100, choices=DEGREE_CHOICES, blank=True, null=True)

# 當使用者註冊時，自動建立一個Dashboard
@receiver(post_save, sender=User)
def create_user_dashboard(sender, instance, created, **kwargs):
    if created:
        DashBoard.objects.create(user=instance)