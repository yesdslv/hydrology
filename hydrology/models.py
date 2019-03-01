from django.db import models
from django.contrib.auth.models import User

from .weather_and_condition_types import PRECIPITATION_TYPES, WIND_POWER_TYPES, WIND_DIRECTION_TYPES

class Hydrologist(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)

    class Meta:
        db_table = 'hydrologists'
    def __str__(self):
        return ' '.join(['Наблюдатель: ', self.user.username, ])

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
#This model describes which hydroposts are observed
#by which hydrologist.
#Basically who(which hydrologist observers), where(which hydropost is observed) 
class Observation(models.Model):
    hydropost = models.ForeignKey(Hydropost, on_delete = models.CASCADE)
    hydrologist = models.ForeignKey(Hydrologist, on_delete = models.CASCADE)

    class Meta:
        db_table = 'observations'
    def __str__(self):
        return ' '.join(['Наблюдение соверашается ', self.hydrologist.user.username, 'на', self.hydropost.name,])

#Basic class that holds basic measurement information
#Observation date and time, when actual observation is made
#Entry date and time, when data is submitted to database
#Time zone is UTC
class AbstractMeasurement(models.Model):
    observation_datetime = models.DateTimeField()
    entry_datetime = models.DateTimeField()
    observation = models.ForeignKey(Observation, on_delete = models.DO_NOTHING)

    class Meta:
        unique_together = ('observation','observation_datetime')
        abstract = True
        
class Level(AbstractMeasurement):
    level = models.DecimalField(max_digits = 5, decimal_places = 2)
    pile = models.IntegerField(null = True)

    class Meta(AbstractMeasurement.Meta):
        db_table = 'level'

class Discharge(AbstractMeasurement):
    discharge = models.DecimalField(max_digits = 5, decimal_places = 2)

    class Meta(AbstractMeasurement.Meta):
        db_table = 'discharge'

class Ripple(AbstractMeasurement):
    ripple = models.IntegerField()

    class Meta(AbstractMeasurement.Meta):
        db_table = 'ripple'

class WaterTemperature(AbstractMeasurement):
    water_temperature = models.DecimalField(max_digits = 5, decimal_places = 2)

    class Meta(AbstractMeasurement.Meta):
        db_table = 'water_temperature'

class AirTemperature(AbstractMeasurement):
    air_temperature = models.DecimalField(max_digits = 5, decimal_places = 2)

    class Meta(AbstractMeasurement.Meta):
        db_table = 'air_temperature'

class IceThickness(AbstractMeasurement):
    ice_thickness = models.IntegerField()

    class Meta(AbstractMeasurement.Meta):
        db_table = 'ice_thickness'

class Precipitation(AbstractMeasurement):
    precipitation = models.DecimalField(max_digits = 5, decimal_places = 2)
    precipitation_type = models.CharField(max_length = 31, choices = PRECIPITATION_TYPES) 

    class Meta(AbstractMeasurement.Meta):
        db_table = 'precipitation'

class Wind(AbstractMeasurement):
    wind_direction = models.CharField(max_length = 17, choices = WIND_DIRECTION_TYPES)
    wind_power = models.CharField(max_length = 10, choices = WIND_POWER_TYPES) 

    class Meta(AbstractMeasurement.Meta):
        db_table = 'wind'

class Comment(AbstractMeasurement):
    comment = models.CharField(max_length = 255)

    class Meta(AbstractMeasurement.Meta):
        db_table = 'comment'
