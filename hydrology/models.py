# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User

class Region(models.Model):
    code = models.CharField(primary_key = True, max_length = 31)
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'regions'

class Hydropost(models.Model):
    code = models.IntegerField(primary_key = True)
    nameEn = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    lat = models.DecimalField(max_digits = 5, decimal_places=2)
    lon = models.DecimalField(max_digits = 5, decimal_places=2)
    region = models.ForeignKey(Region, on_delete = models.DO_NOTHING)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'hydroposts'

class Hydrologist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    region = models.ForeignKey(Region, on_delete = models.DO_NOTHING)

    class Meta:
        db_table = 'hydrologists'

class Discharge(models.Model):
    discharge = models.DecimalField(max_digits = 5, decimal_places = 2)
    observationDate = models.DateTimeField()
    hydrologist = models.ForeignKey(Hydrologist, models.DO_NOTHING)
    hydropost = models.ForeignKey(Hydropost, on_delete = models.DO_NOTHING)

    class Meta:
        db_table = 'discharge'
        unique_together = (('hydropost', 'observationDate'),)


class Level(models.Model):
    level = models.DecimalField(max_digits = 5, decimal_places = 2)
    observationDate = models.DateTimeField()
    hydrologist = models.ForeignKey(Hydrologist, on_delete = models.DO_NOTHING)
    hydropost = models.ForeignKey(Hydropost, on_delete = models.DO_NOTHING)

    class Meta:
        db_table = 'level'
        unique_together = (('hydropost', 'observationDate'),)



