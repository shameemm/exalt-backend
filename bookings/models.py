from django.db import models
from turf.models import TurfDetails
from accounts.models import UserData
# Create your models here.

class Bookings(models.Model):
    user = models.ForeignKey(UserData, on_delete=models.CASCADE)
    turf = models.ForeignKey(TurfDetails, on_delete=models.CASCADE)
    court = models.CharField(max_length=10)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    cash = models.DecimalField(max_digits=10, decimal_places=2)
    is_canceled = models.BooleanField(default=False)