from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from .models import UserRoles, UserProfile

class UserForm(ModelForm):

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

class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')