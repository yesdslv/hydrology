from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from datetime import datetime

from .weather_and_condition_types import PRECIPITATION_TYPES, WIND_DIRECTION_TYPES, WIND_POWER_TYPES 
from .weather_and_condition_types import CONDITION_TYPES, PILE_NUMBERS


#All forms for observation
class MeasurementForm(forms.Form):
    level = forms.DecimalField(widget = forms.NumberInput(attrs =
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
    
    ripple = forms.IntegerField(widget = forms.NumberInput(attrs = 
        {
            'class': 'form-control',
            'placeholder': 'Волнения воды',
        }
    ), required = False, label = False)

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

    #2 water object conditions can be sumbitted
    water_object_condition = forms.MultipleChoiceField(widget = forms.SelectMultiple(attrs=
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
    
    def clean_water_object_condition(self):
        water_object_condition = self.cleaned_data['water_object_condition']
        if len(water_object_condition) > 0 and len(water_object_condition) < 3:
            water_object_condition = ';'.join(water_object_condition)
        else:
            water_object_condition = None
        return water_object_condition

    #Convert list to string
    def clean_wind_power(self):
        wind_power = self.cleaned_data['wind_power']
        if len(wind_power) == 1:
            wind_power = ''.join(wind_power)
        else:
            wind_power = None
        return wind_power

    def clean_wind_direction(self):
        wind_direction = self.cleaned_data['wind_direction']
        if len(wind_direction) == 1:
            wind_direction = ''.join(wind_direction)
        else:
            wind_direction = None
        return wind_direction

    def clean_pile(self):
        pile = self.cleaned_data['pile']
        if len(pile) == 1:
            pile = ''.join(pile)
        else:
            pile = None
        return pile

    def clean_precipitation_type(self):
        precipitation_type = self.cleaned_data['precipitation_type']
        if len(precipitation_type) == 1:
            precipitation_type = ''.join(precipitation_type)
        else:
            precipitation_type = None
        return precipitation_type

##Abbreviations for hydropost categories
##RHP - River HydroPost(Речной пост)
##LHP - Lake HydroPost(Озерный пост)
##SHP - Sea HydroPost(Морской пост)

#Form for Hydropost category RHP1(Речной пост 1 разряд)
class RHP1Form(MeasurementForm):
    class Meta:
        exclude = ('ripple',)

#Form for Hydropost category RHP2(Речной пост 2 разряд)
class RHP2Form(MeasurementForm):
    class Meta:
        exclude = ('ripple',)

#Form for Hydropost category RHP3(Речной пост 3 разряд)
class RHP3Form(MeasurementForm):
    class Meta:
        exclude = ('ripple', 'precipitation', 'precipitation_type',)

#Form for Hydropost category LHP1(Озерный пост 1 разряд)
class LHP1Form(MeasurementForm):
    class Meta:
        exclude = ()

#Form for Hydropost category LHP2(Озерный пост 2 разряд)
class LHP2Form(MeasurementForm):
    class Meta:
        exclude = ()

#Form for Hydropost category SHP1(Морской пост 1 разряд)
class SHP1Form(MeasurementForm):
    class Meta:
        exclude = ()

#Form for Hydropost category SHP2(Морской пост 2 разряд)
class SHP2Form(MeasurementForm):
    class Meta:
        exclude = ()


class StartEndDateTimeForm(forms.Form):
    start_datetime = forms.DateTimeField()
    end_datetime = forms.DateTimeField()
