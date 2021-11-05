from django import forms
from django.forms import ModelForm, DateInput
from .models import UserRoles, UserProfile

class userForm(ModelForm):

    class Meta:
        model = UserProfile
        exclude = ['user']         # Will be taken from the request
        fields = ('title', 'phone',)
        labels = {
            'title': 'Type of member',
            'phone': 'phone number',
            }
        widgets = {
            # 'studentID': forms.Select(attrs={'class':'form-select'}),
            'title': forms.Select(attrs={'class':'form-select'}),

        }

