from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

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