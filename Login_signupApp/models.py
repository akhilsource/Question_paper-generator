from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=50,blank=False,null=False)
    regno = models.CharField(max_length=50, blank=False, null=False, unique=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    password=models.CharField(max_length=50,blank=False,null=False)
    def __str__(self):
        return self.regno
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)