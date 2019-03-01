from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime

from .weather_and_condition_types import PRECIPITATION_TYPES, WIND_DIRECTION_TYPES, WIND_POWER_TYPES 
from .weather_and_condition_types import CONDITION_TYPES, PILE_NUMBERS

from .models import Level
#Minimum forms for observation
class BasicObservationForm(forms.Form):
    level = forms.IntegerField(widget = forms.NumberInput(attrs =
        {
            'class': 'form-control',
            'placeholder': 'Уровень воды(см)',
        }
    ), validators = 
        [
            MaxValueValidator(10000, 'Проверьте уровень воды'),
            MinValueValidator(-1000, 'Проверьте уровень воды'),
        ]
    , label = False, error_messages={'required': 'Уровень обязателен к заполнению'})

    pile = forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs = 
        {
            'class': 'selectpicker',
            'data-none-selected-text': 'Номер сваи',
            'data-max-options-text': 'Выбрать можно только одну сваю',
            'data-max-options': '1',
         #   'data-width': '40%',
        }
    ), choices = PILE_NUMBERS, required = False, label = False)

    water_temperature = forms.DecimalField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Температура воды °С',
        }
    ), validators = 
        [
            MaxValueValidator(50, 'Проверьте температуру воды'),
            MinValueValidator(-5, 'Проверьте температуру воды'),
        ]
    , required = False, label = False)

    ice_thickness = forms.IntegerField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Толщина льда(см)',
        }
    ), validators = 
        [
            MaxValueValidator(180, 'Проверьте толщину льда'),
            MinValueValidator(0, 'Проверьте толщину льда')
        ]
    , required = False, label = False)

class AirTemperatureForm(forms.Form):
    air_temperature = forms.DecimalField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Температура воздуха °С',
        }
    ), validators = 
        [
            MaxValueValidator(60, 'Проверьте температуру воздуха'),
            MinValueValidator(-60, 'Проверьте температуру воздуха')
        ]
    , required = False, label = False)
    
class RippleForm(forms.Form):
    ripple = forms.IntegerField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Волнения воды',
        }
    ), required = False, label = False)

class DischargeForm(forms.Form):
    discharge = forms.DecimalField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Расход воды',
        }
    ), required = False, label = False)

class PrecipitationForm(forms.Form):
    precipitation = forms.DecimalField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Осадки(см)',
        }
    ), validators = 
        [
            MaxValueValidator(1000, 'Проверьте количество осадков'),
            MinValueValidator(0, 'Проверьте количество осадков')
        ]
    , required = False, label = False)

    precipitation_type = forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs=
        { 
            'class': 'selectpicker',
            'data-none-selected-text': 'Тип осадков',
            'data-max-options': '1',
            'data-max-options-text': 'Выбрать можно только один параметр',
            'data-width': '100%',
        }
    ), choices = PRECIPITATION_TYPES, required = False, label = False)

    def clean(self):
         cleaned_data = super().clean()
         precipitation = cleaned_data.get('precipitation', False)
         precipitation_type = cleaned_data.get('precipitation_type', False)
   
         #Checks if precipitation field is empty and precipitation_type field is not empty
         if precipitation is None and precipitation_type:
             raise forms.ValidationError('Заполните все поля осадков')
         #Checks if precipitation field is not empty and precipitation_type field is empty
         if precipitation is not None and not precipitation_type:
             raise forms.ValidationError('Заполните все поля осадков')

class WindForm(forms.Form):
    wind_direction = forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs=
        {
            'class': 'selectpicker',
            'data-none-selected-text': 'Направление ветра',
            'data-max-options': '1',
            'data-max-options-text': 'Выбрать можно только один параметр',
            'data-width': '100%',
        }
    ), choices = WIND_DIRECTION_TYPES, required = False, label = False)
    wind_power = forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs=
        {
            'class': 'selectpicker',
            'data-none-selected-text': 'Сила ветра',
            'data-max-options': '1',
            'data-max-options-text': 'Выбрать можно только один параметр',
            'data-width': '100%',
        }
    ), choices = WIND_POWER_TYPES, required = False, label = False)

class ConditionForm(forms.Form):
    #2 water object conditions can be sumbitted
    condition = forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs=
        {
            'class': 'selectpicker',
            'data-none-selected-text': 'Состояние водного объекта',
            'width': 'fit',
            'data-live-search': 'true',
            'data-max-options': '2',
            'data-multiple-separator': '|',
            'data-max-options-text': 'Максимум 2 состояния водного объекта',
            'data-size': '8',
            'data-width': '100%',
            }
    ), choices = CONDITION_TYPES, required = False, label = False)


##Abbreviations for hydropost categories
##RHP - River HydroPost(Речной пост)
##LHP - Lake HydroPost(Озерный пост)
##SHP - Sea HydroPost(Морской пост)

#Form for Hydropost category RHP1(Речной пост 1 разряд)
class RHP1Form(ConditionForm, WindForm, PrecipitationForm, AirTemperatureForm, BasicObservationForm):
    pass
    
#Form for Hydropost category RHP2(Речной пост 2 разряд)
class RHP2Form(ConditionForm, WindForm, PrecipitationForm, AirTemperatureForm, BasicObservationForm):
    pass

#Form for Hydropost category RHP3(Речной пост 3 разряд)
class RHP3Form(ConditionForm, WindForm, AirTemperatureForm, BasicObservationForm):
    pass

#Form for Hydropost category LHP1(Озерный пост 1 разряд)
class LHP1Form(ConditionForm, WindForm, PrecipitationForm, RippleForm, AirTemperatureForm, BasicObservationForm):
    pass

#Form for Hydropost category LHP2(Озерный пост 2 разряд)
class LHP2Form(ConditionForm, WindForm, PrecipitationForm, RippleForm, AirTemperatureForm, BasicObservationForm):
    pass

#Form for Hydropost category SHP1(Морской пост 1 разряд)
class SHP1Form(ConditionForm, WindForm, PrecipitationForm, RippleForm, AirTemperatureForm, BasicObservationForm):
    pass

#Form for Hydropost category SHP2(Морской пост 2 разряд)
class SHP2Form(ConditionForm, WindForm, PrecipitationForm, RippleForm, AirTemperatureForm, BasicObservationForm):
    pass
