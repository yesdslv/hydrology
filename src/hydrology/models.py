from django.db import models
from django.contrib.auth.models import User

from .weather_and_condition_types import PRECIPITATION_TYPES, WIND_POWER_TYPES, WIND_DIRECTION_TYPES, CONDITION_TYPES


class Hydrologist(models.Model):
    OBSERVER  = 'Наблюдатель'
    ENGINEER = 'Инженер'
    OCCUPATION_TYPES = (
        (OBSERVER, 'Наблюдатель'),
        (ENGINEER, 'Инженер'),
    )
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    occupation = models.CharField(
            max_length= 15, 
            choices = OCCUPATION_TYPES,
            default = OBSERVER,
    )
    
    class Meta:
        db_table = 'hydrologists'
    def __str__(self):
        return ' '.join(['Гидролог: ', self.user.username, ])


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
    #TODO Review realtionship to onetoone
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
    #TODO Review realtionship to onetoone
    hydropost = models.ForeignKey(Hydropost, on_delete = models.CASCADE)
    hydrologist = models.ForeignKey(Hydrologist, on_delete = models.CASCADE)

    class Meta:
        db_table = 'observations'
    def __str__(self):
        return ' '.join(['Наблюдение соверашается ', self.hydrologist.user.username, 'на', self.hydropost.name,])

#Class that holds all observation record related information
#Observation date and time, when actual observation is made
#Entry date and time, when data is submitted to database
#Time zone is UTC
class Measurement(models.Model):
    observation_datetime = models.DateTimeField()
    entry_datetime = models.DateTimeField()
    observation = models.ForeignKey(Observation, on_delete = models.DO_NOTHING)
    level = models.IntegerField()
    pile = models.IntegerField(blank = True, null = True)
    ripple = models.IntegerField(blank = True, null = True)
    water_temperature = models.DecimalField(max_digits = 5, decimal_places = 2,blank = True, null = True)
    air_temperature = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True)
    ice_thickness = models.IntegerField(blank = True, null = True)
    precipitation = models.DecimalField(max_digits = 5, decimal_places = 2, blank = True, null = True)
    precipitation_type = models.CharField(max_length = 31, choices = PRECIPITATION_TYPES, blank = True, null = True) 
    wind_direction = models.CharField(max_length = 17, choices = WIND_DIRECTION_TYPES, blank = True, null = True)
    wind_power = models.CharField(max_length = 10, choices = WIND_POWER_TYPES, blank = True, null = True) 
    #Observer can submit 2 water object conditions
    #Combine in case of 2 water object conditions to 1 string separated by ;(semicolon)
    water_object_condition = models.CharField(max_length = 200, choices = CONDITION_TYPES, blank = True, null = True)
    comment = models.CharField(max_length = 255, blank = True, null = True)

    class Meta:
        unique_together = ('observation','observation_datetime')
        db_table = 'measurements'
                
class Discharge(models.Model):
    discharge = models.DecimalField(max_digits = 5, decimal_places = 2)

    class Meta():
        db_table = 'discharge'
