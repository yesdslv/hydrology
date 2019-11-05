from django.db import models


class Meteopost(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

class MeteopostPhoto(models.Model):
