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

class AirTemperatureForm(forms.Form):
    air_temperature = forms.DecimalField(label = 'Температура воздуха', required = False)
    
class RippleForm(forms.Form):
    ripple = forms.IntegerField(label = 'Волнения воды', required = False)

class DischargeForm(forms.Form):
    discharge = forms.DecimalField(label = 'Расход воды', required = False)

class PrecipitationForm(forms.Form):
    precipitation = forms.CharField(label = 'Атмосферные осадки', required = False)



#Form for Hydropost category GP1(Речной пост 1 разряд)
class GP1Form(BasicObservationForm,  DischargeForm, AirTemperatureForm):
    pass
#Form for Hydropost category OGP1(Озерный пост 2 разряд)
class OGP2Form(BasicObservationForm, AirTemperatureForm, RippleForm):
    pass
