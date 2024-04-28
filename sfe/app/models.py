from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class User_otherfields(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile_image=models.ImageField(upload_to="static" , null=True)
    cni=models.CharField(max_length=10,blank=True)
    

    def __str__(self):
        return self.user.username
