from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from django.db import IntegrityError

from datetime import datetime, timedelta

from collections import OrderedDict

from .models import Hydrologist, Hydropost, Observation, Measurement
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
            Measurement.objects.create(
                level = form.cleaned_data.get('level'),
                pile = form.cleaned_data.get('pile'),
                water_temperature = form.cleaned_data.get('water_temperature'),
                ice_thickness = form.cleaned_data.get('ice_thickness'),
                air_temperature = form.cleaned_data.get('air_temperature'),
                ripple = form.cleaned_data.get('ripple'),
                precipitation = form.cleaned_data.get('precipitation'),
                precipitation_type = form.cleaned_data.get('precipitation_type'),
                wind_direction = form.cleaned_data.get('wind_direction'),
                wind_power = form.cleaned_data.get('wind_power'),
                water_object_condition = form.cleaned_data.get('water_object_condition'),
                observation_datetime= observation_datetime,
                entry_datetime = entry_datetime,
                observation= observation,
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
    if request.method == 'POST' and request.is_ajax():
        form = StartEndDateTimeForm(request.POST)
        #for key in request.POST:
        #    print('Key is ' + str(key))
        #    print('Value is ' + str(request.POST.get(key, False)))
        start_datetime = request.POST.get('start_datetime', False)
        end_datetime = request.POST.get('end_datetime', False)
        #Used in pagination(limit the query(start,length)), 
        #By which column ordered(index is passed),
        #Order direction(asc or desc)
        #In search hydropost column  and show requested page
        start = request.POST.get('start', False)
        length = request.POST.get('length', False)
        column_index_order = request.POST.get('order[0][column]', False)
        order_dir = request.POST.get('order[0][dir]',False)
        search_value = request.POST.get('search[value]', False)
        #TODO validate that int type variable passed
        start = int(start)
        length = int(length)
        end = start + length
        column_index_order = int(column_index_order)
        if order_dir == 'asc':
            order_dir = ''
        elif order_dir == 'desc':
            order_dir = '-'
        #Order of list is important
        #Order of list is related to order of columns in datatable
        field_list = [
            'observation__hydropost__region__name',
            'observation__hydrologist__user__first_name',
            'observation__hydrologist__user__last_name',
            'entry_datetime',
            'observation__hydropost__name', 
            'observation_datetime', 
            'level',
            'water_object_condition',
            'air_temperature',
            'water_temperature',
            'precipitation',
            'precipitation_type',
            'wind_direction',
            'wind_power',
        ]
        #Add 3, cause order is not considered for first three elements,
        measurements = Measurement.objects.filter(
            observation_datetime__range = [start_datetime, end_datetime],
            observation__hydropost__name__icontains = search_value
        ).order_by(order_dir + field_list[column_index_order + 3]
        ).values(*field_list)
        total_records = Measurement.objects.count() 
        result_json = OrderedDict()
        #Used for pagination
        result_json['draw'] = request.POST.get('draw', False) 
        result_json['recordsTotal'] = total_records
        result_json['recordsFiltered'] = len(measurements) 
        result_json['data'] = []
        measurements = measurements[start:end]
        for measurement in measurements:
            #Rename some keys
            measurement['hydropost_name'] = measurement.pop('observation__hydropost__name')
            measurement['region'] = measurement.pop('observation__hydropost__region__name')
            first_name = measurement.pop('observation__hydrologist__user__first_name')
            last_name = measurement.pop('observation__hydrologist__user__last_name')
            measurement['observer'] = str(first_name) + " " + str(last_name)
            result_json['data'].append(measurement)
        return JsonResponse(result_json)
    elif request.method == 'GET':
        form = StartEndDateTimeForm()
    context = { 'form' : form, }
    return render(request, 'hydrology/data.html', context)
