from django import forms

#Minimum forms for observation
class BasicObservationForm(forms.Form):
    level = forms.IntegerField(label = 'Уровень воды')
    water_temperature = forms.DecimalField(label = 'Температура воды',
            max_digits = 5, 
            decimal_places = 2, 
            max_value = 70, 
            min_value = -70,
            required = False)
    ice_thickness = forms.IntegerField(label = 'Толщина льда', required = False)

class AirTemperatureForm(forms.Form):
    air_temperature = forms.DecimalField(label = 'Температура воздуха', required = False)
    
class RippleForm(forms.Form):
    ripple = forms.IntegerField(label = 'Волнения воды', required = False)

class DischargeForm(forms.Form):
    discharge = forms.DecimalField(label = 'Расход воды', required = False)

class PrecipitationForm(forms.Form):
    precipitation = forms.CharField(label = 'Атмосферные осадки', required = False)



##Abbreviations for hydropost categories
##RHP - River HydroPost(Речной пост)
##LHP - Lake HydroPost(Озерный пост)
##SHP - Sea HydroPost(Морской пост)

#Form for Hydropost category RHP1(Речной пост 1 разряд)
class RHP1Form(BasicObservationForm, DischargeForm, AirTemperatureForm):
    pass

#Form for Hydropost category RHP2(Речной пост 2 разряд)
class RHP2Form(BasicObservationForm, AirTemperatureForm):
    pass

#Form for Hydropost category RHP3(Речной пост 3 разряд)
class RHP3Form(BasicObservationForm, AirTemperatureForm):
    pass

#Form for Hydropost category LHP1(Озерный пост 1 разряд)
class LHP1Form(BasicObservationForm, RippleForm, AirTemperatureForm):
    pass

#Form for Hydropost category LHP2(Озерный пост 2 разряд)
class LHP2Form(BasicObservationForm, RippleForm, AirTemperatureForm):
    pass

#Form for Hydropost category SHP1(Морской пост 1 разряд)
class SHP1Form(BasicObservationForm, RippleForm, AirTemperatureForm):
    pass

#Form for Hydropost category SHP2(Морской пост 2 разряд)
class SHP2Form(BasicObservationForm, RippleForm, AirTemperatureForm):
    pass
