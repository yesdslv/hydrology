from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from .models import Hydrologist

#Decorator for views that checks that the logged in user is a observer,
#redirects to the log-in page if necessary.
def observer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and Hydrologist.objects.get(user = u).occupation == Hydrologist.OBSERVER,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


#Decorator for views that checks that the logged in user is a teacher,
#redirects to the log-in page if necessary.
def engineer_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='login'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and Hydrologist.objects.get(user = u).occupation == Hydrologist.ENGINEER,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
