from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import Hydrologist, Hydropost
from .forms import RHP1Form, RHP2Form, RHP3Form, LHP1Form, LHP2Form, SHP1Form, SHP2Form

#This list is used record view for getting required form
list_form = {'Речной пост 1 разряд' : RHP1Form, 
        'Речной пост 2 разряд' : RHP2Form, 
        'Речной пост 3 разряд' : RHP3Form,
        'Морской пост 1 разряд' : SHP1Form,
        'Морской пост 2 разряд' : SHP2Form,
        'Озерный пост 1 разряд' : LHP1Form,
        'Озерный пост 2 разряд' : LHP2Form,
        }    

@login_required(login_url = '/login/')
def home(request):
    user = request.user
    hydrologist = Hydrologist.objects.get(user = user)
    hydroposts = hydrologist.hydropost_set.all()
    context = { 'hydroposts' : hydroposts ,}
    return render(request, 'hydrology/home.html', context)

@login_required(login_url = '/login/')
def record(request):
    if request.method == 'POST':
       category = request.GET.get('category', False)   
       form = list_form[h_type](request.POST)
       if form.is_valid():
          return redirect('/')
    elif request.method == 'GET':
       category = request.GET.get('category', False) 
       #TODO
       #Add render in case of absence of key in list_form
       try:
          form = list_form[category]()
       except KeyError:
          print('error')       
    context = { 'form' : form }
    return render(request, 'hydrology/record.html', context) 

@login_required(login_url = '/login/')
def search_hydropost_type(request):
    if request.method == 'GET':
        try:
            hydropost = Hydropost.objects.get(nameEn = request.GET.get('hydropost', False))
            data = { 'category' : hydropost.category.name, }
        except Hydropost.DoesNotExist:
            data = { 'error' : 'Нет такой станции', }
        return JsonResponse(data)
