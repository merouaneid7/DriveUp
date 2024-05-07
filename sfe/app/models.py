from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class User_otherfields(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile_image=models.ImageField(upload_to="static" , null=True)
    cni=models.CharField(max_length=10,blank=True)
    

    def __str__(self):
        return self.user.username

class Course(models.Model):
    title = models.CharField(max_length=100,null=True)
    thumbnail=models.ImageField(upload_to="static" , null=True)
    price=models.IntegerField(null=True)
    description = models.TextField(null=True)


    def clean(self):
        super().clean()
        if Course.objects.count() >= 3:
            raise ValidationError("Maximum of 3 courses allowed.")
        

class Part(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100,null=True)
    thumbnail=models.ImageField(upload_to="static" , null=True)

    def clean(self):
        super().clean()
        if Part.objects.filter(course=self.course).count() >= 4:
            raise ValidationError("Maximum of 4 parts per course allowed.")
        

class Lesson(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=100,null=True)
    thumbnail=models.ImageField(upload_to="static" , null=True)



class Appointement(models.Model):
    accepted=models.BooleanField(default=False)
    nom=models.CharField(max_length=20,null=True)
    prenom=models.CharField(max_length=30,null=True)
    cni=models.CharField(max_length=10,null=True)
    numero_telephone=models.IntegerField(null=True)
    email=models.EmailField(max_length=20,null=True)
    message=models.CharField(max_length=40,null=True)
    date=models.DateField(null=True)