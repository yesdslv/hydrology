from django.contrib import admin

from .models import Hydrologist, Region, HydropostCategory, Hydropost, Observation, Discharge

admin.site.register(Hydrologist)
admin.site.register(Region)
admin.site.register(HydropostCategory)
admin.site.register(Hydropost)
admin.site.register(Observation)
admin.site.register(Discharge)

