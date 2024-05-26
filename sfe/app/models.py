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
    



class Appointement(models.Model):
    accepted=models.BooleanField(default=False)
    nom=models.CharField(max_length=20,null=True)
    prenom=models.CharField(max_length=30,null=True)
    cni=models.CharField(max_length=10,null=True)
    numero_telephone=models.IntegerField(null=True)
    email=models.EmailField(max_length=20,null=True)
    message=models.CharField(max_length=40,null=True)
    date=models.TextField(null=True)



class Driver(models.Model):
    CAR = 'Voiture'
    MOTO = 'Moto'
    POIDS_LOURD = 'Poids Lourd'

    VEHICLE_CHOICES = [
        (CAR ,'Voiture'),
        (MOTO ,'Moto'),
        (POIDS_LOURD ,'Poids lourd'),
    ]

    Artiste_du_Volant='Artiste du Volant'
    Maitre_Conducteur='Maitre Conducteur'
    Expert_au_Volant='Expert au Volant'

    LEVEL_CHOICES=[
        (Artiste_du_Volant, 'Artiste du Volant'),
        (Maitre_Conducteur, 'Maitre Conducteur'),
        (Expert_au_Volant, 'Expert au Volant'),
    ]


    
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    level=models.CharField(max_length=20,choices=LEVEL_CHOICES,null=True)
    is_driver=models.BooleanField(null=True)
    vehicle = models.CharField(max_length=20, choices=VEHICLE_CHOICES,null=True)

    def __str__(self):
        return self.user.username

    

class Driving_offer(models.Model):
    conduite_de_base='conduite de base'
    conduite_sur_ville='conduite sur ville'
    conduite_sur_circuit='conduite sur circuit'
    
    driving_offer_CHOICES=[
        (conduite_de_base,'conduite de base'),
        (conduite_sur_ville,'conduite sur ville'),
        (conduite_sur_circuit,'conduite sur circuit'),
    ]


    driver=models.ForeignKey(Driver,on_delete=models.CASCADE,null=True)
    offer_type=models.CharField(max_length=30,choices=driving_offer_CHOICES)
    price_per_hour=models.IntegerField(null=True)
    is_active=models.BooleanField(null=True,default=False)
    def __str__(self):
        return self.driver.user.username


class Request_driving_offer(models.Model):
    driving_offer = models.ForeignKey(Driving_offer, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    time=models.TimeField(null=True)
    vehicle_name=models.CharField(max_length=50,null=True)
    date=models.TextField(null=True)
    is_approuved=models.BooleanField(default=False,null=True)

    def __str__(self):
        return self.user.username
    



class Car(models.Model):
    DEBUTANT='Debutant'
    INTERMIDIAIRE='Intermidiare'
    AVANCE='Avance'
    
    vehicle_level_CHOICES=[
        (DEBUTANT,'Debutant'),
        (INTERMIDIAIRE,'Intermidiare'),
        (AVANCE,'Avance'),
    ]
    name=models.CharField(max_length=50,null=True)
    level=models.CharField(max_length=20,null=True,choices=vehicle_level_CHOICES)
  


class Bike(models.Model):
    DEBUTANT='Debutant'
    INTERMIDIAIRE='Intermidiare'
    AVANCE='Avance'
    
    vehicle_level_CHOICES=[
        (DEBUTANT,'Debutant'),
        (INTERMIDIAIRE,'Intermidiare'),
        (AVANCE,'Avance'),
    ]
    name=models.CharField(max_length=50,null=True)
    level=models.CharField(max_length=20,null=True,choices=vehicle_level_CHOICES)

class Truck(models.Model):
    DEBUTANT='Debutant'
    INTERMIDIAIRE='Intermidiare'
    AVANCE='Avance'
    
    vehicle_level_CHOICES=[
        (DEBUTANT,'Debutant'),
        (INTERMIDIAIRE,'Intermidiare'),
        (AVANCE,'Avance'),
    ]
    name=models.CharField(max_length=50,null=True)
    level=models.CharField(max_length=20,null=True,choices=vehicle_level_CHOICES)

class subscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email=models.EmailField(null=True, max_length=254)