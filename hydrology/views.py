from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Hydrologist

@login_required(login_url = '/login/')
def home(request):
    user = request.user
    hydrologist = Hydrologist.objects.get(user = user)
    hydroposts = hydrologist.hydropost_set.all()
    context = { 'hydroposts' : hydroposts ,}
    return render(request, 'hydrology/home.html', context)
