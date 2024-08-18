from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=1000)
    image = models.CharField(max_length=1000, default="../img/default.jpg")
    listing_id = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    price = models.FloatField()
    rating = models.CharField(default="", max_length=100)
    liked_by = models.ManyToManyField(User, related_name='liked_listings')
    check_in = models.CharField(max_length=10, default="01/01/2025")
    check_out = models.CharField(max_length=10, default="01/01/2025")
    adults = models.IntegerField(default=0)
    children = models.IntegerField(default=0)
    infants = models.IntegerField(default=0)
    pets = models.IntegerField(default=0)   


    

    