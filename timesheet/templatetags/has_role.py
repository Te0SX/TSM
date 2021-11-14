from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_role')
def has_role(user,role_name):
    userRole = str(user.userprofile.title)
    if userRole == role_name:
        return True
    else:
        return False