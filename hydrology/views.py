from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Hydrologist, Hydropost

@login_required(login_url = '/login/')
def home(request):
    user = request.user
    hydrologist = Hydrologist.objects.get(user = user)
    hydroposts = hydrologist.hydropost_set.all()
    context = { 'hydroposts' : hydroposts ,}
    return render(request, 'hydrology/home.html', context)

@login_required(login_url = '/login/')
def record(request):
    hydropost = get_object_or_404(Hydropost, nameEn = request.POST.get('hydropost', False))
    context = { 'hydropost' : hydropost ,}
    return render(request, 'hydrology/record.html', context)
