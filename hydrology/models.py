from django.db import models
from django.contrib.auth.models import User

class Hydrologist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    class Meta:
        db_table = 'hydrologists'

class Region(models.Model):
    code = models.CharField(primary_key = True, max_length = 31)
    name = models.CharField(max_length = 255)

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'regions'

class HydropostCategory(models.Model):
    code = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=255)
        
    def __str__(self):
        return self.name
    class Meta:
        db_table = 'hydropost_categories'

class Hydropost(models.Model):
    code = models.IntegerField(primary_key = True)
    nameEn = models.CharField(max_length = 255)
    name = models.CharField(max_length = 255)
    lat = models.DecimalField(max_digits = 5, decimal_places=2)
    lon = models.DecimalField(max_digits = 5, decimal_places=2)
    region = models.ForeignKey(Region, on_delete = models.DO_NOTHING)
    category = models.ForeignKey(HydropostCategory, on_delete = models.DO_NOTHING)
    hydrologists = models.ManyToManyField(
                    Hydrologist,
                    through = 'Observation',
                    through_fields = ('hydropost', 'hydrologist'),
                    )

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'hydroposts'

#Observation contains hydrologist and hydropost
#This model contain list, which hydroposts can be observed
#by which hydrologist
class Observation(models.Model):
    hydropost = models.ForeignKey(Hydropost, on_delete = models.CASCADE)
    hydrologist = models.ForeignKey(Hydrologist, on_delete = models.CASCADE)

    class Meta:
        db_table = 'observations'

class Discharge(models.Model):
    discharge = models.DecimalField(max_digits = 5, decimal_places = 2)
    observationDate = models.DateTimeField()
    observation = models.ForeignKey(Observation, on_delete = models.DO_NOTHING)

    class Meta:
        db_table = 'discharge'

class Level(models.Model):
    level = models.DecimalField(max_digits = 5, decimal_places = 2)
    observationDate = models.DateTimeField()
    observation = models.ForeignKey(Observation, on_delete = models.DO_NOTHING)

    class Meta:
        db_table = 'level'
