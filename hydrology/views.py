from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import JsonResponse, HttpResponse
from django.db.models import Q
from django.db import IntegrityError

from datetime import datetime, timedelta
import json

from .models import Hydrologist, Hydropost, Observation
from .models import Level, Ripple, WaterTemperature, AirTemperature, IceThickness, Precipitation, Wind, Condition, Comment
from .forms import RHP1Form, RHP2Form, RHP3Form, LHP1Form, LHP2Form, SHP1Form, SHP2Form, StartEndDateTimeForm
from .decorators import observer_required, engineer_required

#This list is used by record view to get required form
list_form = {
        'Речной пост 1 разряд' : RHP1Form, 
        'Речной пост 2 разряд' : RHP2Form, 
        'Речной пост 3 разряд' : RHP3Form,
        'Морской пост 1 разряд' : SHP1Form,
        'Морской пост 2 разряд' : SHP2Form,
        'Озерный пост 1 разряд' : LHP1Form,
        'Озерный пост 2 разряд' : LHP2Form,
        }    

@login_required(login_url = '/login/')
def home(request):
    hydrologist = Hydrologist.objects.get(user =request.user)
    occupation = hydrologist.occupation
    if occupation == Hydrologist.OBSERVER:
            return redirect('observation')
    elif occupation == Hydrologist.ENGINEER:
            return redirect('data')
    #In case Hydrologist occupation field contains non-valid value
    #It renders message 'contact admin'
    return render(request, 'hydrology/home.html') 
    

@login_required(login_url = '/login/')
@observer_required
def observation(request):
    user = request.user
    hydrologist = Hydrologist.objects.get(user = user)
    hydroposts = hydrologist.hydropost_set.all()
    context = { 'hydroposts' : hydroposts ,}
    return render(request, 'hydrology/observation.html', context)

@login_required(login_url = '/login/')
@observer_required
def record(request):
    if request.method == 'POST' and request.is_ajax():
       #By whom observation record is submitted 
       user = request.user
       hydrologist = Hydrologist.objects.get(user = user)
       #Where observation record is submitted
       hydropost_name = request.POST.get('hydropost', False)
       hydropost = Hydropost.objects.get(name = hydropost_name)
       #Observation is combination of who(hydrologist) and where(hydropost)
       observation = Observation.objects.get(Q(hydrologist = hydrologist) & Q(hydropost = hydropost))
       category = request.POST.get('category', False)
       form = list_form[category](request.POST)
       #When data is entered
       entry_datetime = datetime.utcnow()
       #Remove seconds
       entry_datetime = entry_datetime.replace(second = 0)
       #When data is observed
       local_date = request.POST.get('date', False)
       local_hour = request.POST.get('hour', False)
       local_minute = request.POST.get('minute', False)
       observation_datetime = datetime.strptime(local_date, '%Y-%m-%d')
       #Remove seconds and microseconds
       observation_datetime = observation_datetime.replace(second = 0, microsecond = 0)
       #Set hour and minute
       observation_datetime = observation_datetime.replace(hour = int(local_hour), minute = int(local_minute))
       #Difference between hydrologist timezone and UTC
       offset = request.POST.get('minute', False)
       observation_datetime = observation_datetime - timedelta(minutes = int(offset))
       ### print('Observation datetime' + str(observation_datetime))
       ### print('entry_datetime' + str(entry_datetime))
       #Checks if data is not exceed min and max range or all necessary data is submitted
       if form.is_valid():
          try:
            #Json response done(success) status
            status = 200
            print(form.cleaned_data)
            for key, value in form.cleaned_data.items():
                #Do not consider empty fields
                if value is not None:
                    if key == 'ripple':
                        Ripple.objects.create(
                              ripple = value,
                              observation_datetime = observation_datetime,
                              entry_datetime = entry_datetime,
                              observation = observation,
                        )
                    elif key == 'water_temperature':
                        WaterTemperature.objects.create(
                              water_temperature = value,
                              observation_datetime = observation_datetime,
                              entry_datetime = entry_datetime,
                              observation = observation,
                        )
                    elif key == 'air_temperature':
                        AirTemperature.objects.create(
                              air_temperature = value,
                              observation_datetime = observation_datetime,
                              entry_datetime = entry_datetime,
                              observation = observation,
                        )
                    elif key == 'ice_thickness':
                        IceThickness.objects.create(
                              ice_thickness = value,
                              observation_datetime = observation_datetime,
                              entry_datetime = entry_datetime,
                              observation = observation,
                        )
                    elif key == 'comment':
                        Comment.objects.create(
                                comment = value,
                                observation_datetime = observation_datetime,
                                entry_datetime = entry_datetime,
                                observation = observation,
                        )
                    elif key == 'condition' and value:
                        #2 water object condition can be submitted
                        #If 2 water object conditions are submitted,
                        #Combine the in 1 string separated by semicolon(;)
                        condition = ';'.join(value)
                        Condition.objects.create(
                                condition = condition,
                                observation_datetime = observation_datetime,
                                entry_datetime = entry_datetime,
                                observation = observation,
                        )
                    elif key == 'level':
                        level = value
                    elif key == 'precipitation':
                        precipitation = value
                    elif key == 'pile' and value:
                        #Form MultiSelect POST list, get first element in list
                        pile = value[0]
                    elif key == 'precipitation_type' and value:
                        #Form Select POST list, get first element in list
                        precipitation_type = value[0]
                    elif key == 'wind_direction' and value:
                        #Form Select POST list, get first element in list
                        wind_direction = value[0]
                    elif key == 'wind_power' and value:
                        #Form Select POST list, get first element in list
                        wind_power = value[0]
            #Check if variables precipitation and precipitation_type are initialized
            #In dict for loop earlier
            if 'precipitation' in locals() and 'precipitation_type' in locals(): 
                #Thus model Precipitation consists of 'precipitation' and 'precipitation_type' fields
                #And it is required according to observation policy to fill both fields
                #Call Precipiation model object once
                #save 'precipitation' and 'precipitation_type' at the same time  
                Precipitation.objects.create(
                    precipitation = precipitation,
                    precipitation_type = precipitation_type,
                    observation_datetime = observation_datetime,
                    entry_datetime = entry_datetime,
                    observation = observation
                )
            #Check if variables precipitation and precipitation_type are initialized  
            #In dict for loop earlier
            if 'wind_direction' in locals() and 'wind_power' in locals(): 
                #Thus model Wind consists of 'wind_direction' and 'wind_power' fields
                #And it is required according to observation policy to fill both fields
                #Call Wind model object once
                #save 'wind_direction' and 'wind_power' at the same time  
                Wind.objects.create(
                    wind_direction = wind_direction,
                    wind_power = wind_power,
                    observation_datetime = observation_datetime,
                    entry_datetime = entry_datetime,
                    observation = observation
                )
            #Check if variable pile is initialized  
            #In dict for loop earlier
            #Thus model Level consists of 'level' and 'pile' fields
            #Check if pile variable initialized and save level with or without pile data
            if 'pile' in locals():
                Level.objects.create(
                    level = level,
                    pile = pile,
                    observation_datetime = observation_datetime,
                    entry_datetime = entry_datetime,
                    observation = observation
                ) 
            else:
                Level.objects.create(
                    level = level,
                    observation_datetime = observation_datetime,
                    entry_datetime = entry_datetime,
                    observation = observation
                )
            data = { 'done' : 'done',}
          #When observation and observation_date are not unique
          except IntegrityError as error_data:
            status = 500
            error_data = 'Данные уже существуют'
            data = {'error' : error_data}
       else:
          #Json response fail status
          status = 500
          #errors in Dict from form validators
          errors = form.errors.get_json_data()
          error_data = []
          #TODO
          #Review loop over dict
          for value in errors.items():
              error_data.append(str(value[1][0]['message']))
          data = { 'error' : ','.join(error_data)}
       return JsonResponse(data, status = status)
    elif request.method == 'GET':
       category = request.GET.get('category', False) 
       #TODO
       #Add render in case of absence of key in list_form
       try:
          form = list_form[category]()
       except KeyError:
          print('error')       
    context = { 'form' : form, }
    return render(request, 'hydrology/record.html', context) 

@login_required(login_url = '/login/')
@observer_required
def search_hydropost_category(request):
    if request.method == 'GET' and request.is_ajax():
        try:
            hydropost = Hydropost.objects.get(name = request.GET.get('hydropost', False))
            data = { 'category' : hydropost.category.name, }
        except Hydropost.DoesNotExist:
            data = { 'error' : 'Нет такой станции', }
        return JsonResponse(data)
    
@login_required(login_url = '/login/')
@engineer_required
def data(request):
    if request.method == 'GET' and request.is_ajax():
            start_datetime = request.GET.get('start_datetime', False)
            end_datetime = request.GET.get('end_datetime', False)
            print(start_datetime)
            print(end_datetime)
            form = StartEndDateTimeForm()
            level_query_set = Level.objects.filter(observation_datetime__range = 
                    [start_datetime, end_datetime]
            ).values('level', 'observation_datetime', 'entry_datetime')
            data1 = Level.objects.get_table(start_datetime, end_datetime)
            print(data1)
            print(type(data1))
            return JsonResponse(data1)
    elif request.method == 'GET':
            form = StartEndDateTimeForm()
    context = { 'form' : form, }
    return render(request, 'hydrology/data.html', context)
