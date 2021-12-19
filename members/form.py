from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from .models import UserRoles, UserProfile

#Registering Form layout
class RegisterUserForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

# Admin User Role profile view when registering
class UserForm(ModelForm):
    title = forms.Select()
    phone = forms.CharField(max_length=13)
    class Meta:
        model = UserProfile
        exclude = ['user', 'salary',]         # Will be taken from the request
        fields = ('title', 'phone',)
        labels = {
            'title': 'Type of member',
            'phone': 'phone number',
            }
        widgets = {
            # 'studentID': forms.Select(attrs={'class':'form-select'}),
            'title': forms.Select(attrs={'class':'form-select'}),
        }

#Form for the Role of a user
class UserRoleForm(ModelForm):
    title = forms.Select()
    class Meta:
        model = UserProfile
        exclude = ['user', 'salary', 'phone']         # Will be taken from the request
        fields = ('title',)
        labels = {
            'title': 'Type of member',
            }
        widgets = {
            # 'studentID': forms.Select(attrs={'class':'form-select'}),
            'title': forms.Select(attrs={'class':'form-select'}),
        }

# User's phone update, to include this to the User Profile with other details.
class UserFormUpdate(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user', 'salary',]         # Will be taken from the request
        fields = ('phone',)
        labels = {
            'phone': 'phone number',
            }
        widgets = {
            'phone': forms.TextInput(attrs={'placeholder': 'Mobile number', 'box-shadow': 'red'}),

        }

# User's Profile view, with all details to be instanced and able to beupdated.
class UserProfileUpdate(forms.ModelForm):
    email = forms.EmailField()
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)

    class Meta:
        model = User
        exclude = ('password1', 'password2')
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'formclass'}),

        }

# Form for the Update Password view, where only password can change for a user.
class UserPasswordUpdate(UserCreationForm):
    class Meta:
        model = User
        fields = ('password1', 'password2')