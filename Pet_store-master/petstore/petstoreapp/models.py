from django.db import models # type: ignore
from django.contrib.auth.models import User

# Create your models here.

class Pet(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    type = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    gender = models.CharField(max_length=50,default='')
    description = models.CharField(max_length=100,default='')
    petimage = models.ImageField(upload_to="image",default='')

class Cart(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE, db_column='uid')
    petid = models.ForeignKey(Pet, on_delete=models.CASCADE, db_column='petid')
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    orderid = models.CharField(max_length=50)
    userid = models.ForeignKey(User,on_delete=models.CASCADE,db_column='userid')
    petid = models.ForeignKey(Pet,on_delete=models.CASCADE,db_column='petid')
    quantity = models.IntegerField()