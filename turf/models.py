from django.db import models
from django.db.models import Count
from accounts.models import UserData

# Create your models here.
def upload_to(instance, filename):
    return 'images/turf-logo/{filename}'.format(filename=filename)

class Pricing(models.Model):
    fives = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sevens = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    elevens = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cricket = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class TurfDetails(models.Model):
    turf = models.ForeignKey(UserData,on_delete=models.CASCADE , null=True)
    price = models.ForeignKey(Pricing, on_delete=models.CASCADE, null=True)
    place = models.CharField(max_length = 150, null=True)
    lat = models.CharField(max_length = 100, null=True)
    lng = models.CharField(max_length = 100, null=True)
    fives = models.BooleanField(default=False, null=True)
    sevens = models.BooleanField(default=False, null=True)
    elevens = models.BooleanField(default=False, null=True)
    cricket = models.BooleanField(default=False, null=True)
    cafe = models.BooleanField(default=False, null=True)
    first_aid = models.BooleanField(default=False, null=True)
    locker = models.BooleanField(default=False, null=True)
    parking = models.BooleanField(default=False, null=True)
    shower = models.BooleanField(default=False, null=True)
    logo = models.ImageField(upload_to=upload_to, null=True, blank=True)
    approved = models.BooleanField(default=False)
    unlisted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.turf.name
    
class ReviewRatings(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    turf = models.ForeignKey(TurfDetails, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    review = models.CharField(max_length=100, null=True)
    
class Earnings(models.Model):
    turf = models.ForeignKey(TurfDetails, on_delete=models.CASCADE)
    day = models.DateField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=100, default="Ready to withdraw")
    
    
    
    
