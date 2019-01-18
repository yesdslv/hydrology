from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Hydrologist, Hydropost
from .forms import GP1Form, OGP2Form


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
    if request.method == 'POST':
        form = GP1Form()
        if form.is_valid():
            return redirect('/')
    else:
        form = GP1Form()
    context = { 'hydropost' : hydropost ,
                'form': form, }
    return render(request, 'hydrology/record.html', context)

#@login_required(login_url = '/login/')
#def search_hydropost_type(request):
#    if request.method == 'GET':
#        if 'hydropost' in request.GET.keys():
#                message = 'You submitted: %r' % request.GET['q']
#            else:
#                message = 'You submitted nothing!'
#    return HttpResponse(message)
