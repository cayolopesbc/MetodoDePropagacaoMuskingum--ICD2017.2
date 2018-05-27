import sys
from django.db import models

class Coordinate(models.Model):
    x = models.FloatField()
    y = models.FloatField()

class Station(models.Model):
    coordinates = models.ForeignKey(Coordinate)
    drainarea = models.IntegerField(null=True)
    code = models.IntegerField(null=True)
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    __repr__ = __str__

class DataSerie(models.Model):
    station = models.ForeignKey(Station)
    data = models.FloatField(null=True,verbose_name = ('Data'))
    date = models.DateTimeField(verbose_name = ('Date'),unique=False)
    
