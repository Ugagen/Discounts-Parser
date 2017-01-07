from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models


# Create your models here.
class Android(models.Model):
    source = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    date = models.DateTimeField()
    url = models.CharField(max_length=200)
    rating = models.IntegerField()
    star = models.IntegerField()
    halfstar = models.IntegerField()
    price = models.FloatField()
    artist = models.CharField(max_length=200)
    screenshots = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.url
