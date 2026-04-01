from django.db import models

class Passenger(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    source_station = models.CharField(max_length=100)
    destination_station = models.CharField(max_length=100)
    travel_date = models.DateField()
    ticket_price = models.FloatField()

    def __str__(self):
        return self.name
