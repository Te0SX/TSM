from django import template
from django.contrib.auth.models import Group

register = template.Library()

# tags that can check if a user has a specific role through the templates, for different scenarios.
@register.filter(name='has_role')
def has_role(user,role_name):
    userRole = str(user.userprofile.title)
    return userRole == role_name