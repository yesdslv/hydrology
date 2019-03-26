from django import template
from django.db.models import Q

register = template.Library() 

@register.filter(name='has_groups') 
def has_groups(user):
    return user.groups.filter(Q(name = 'engineers') | Q(name = 'observers')).exists() 
