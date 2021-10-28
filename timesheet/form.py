from django import forms
from django.forms import ModelForm, DateInput
from .models import Shift

# Create a Shift form

# class DateForm(forms.Form):
#     date = forms.DateTimeField(
#         input_formats=['%d/%m/%Y %H:%M'],
#         widget=forms.DateTimeInput(attrs={
#             'class': 'form-control datetimepicker-input',
#             'data-target': '#datetimepicker1'
#         })
#     )

class ShiftForm(ModelForm):

    class Meta:
        model = Shift
        fields = ('studentID','role', 'startHour','endHour')

        labels = {'studentID': 'Name of the student'}

        widgets = {
            'studentID': forms.Select(attrs={'class':'form-select'}),
            # 'studentID': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Name of the student'}),
            'role': forms.Select(attrs={'class':'form-select'}),
            # 'startHour': forms.TextInput(attrs={'class' : "form-control datetimepicker-input"}),
            'startHour' : forms.DateTimeInput(attrs={
                    'class': 'form-control datetimepicker-input',
                    'data-target': '#datetimepicker1',
                }),
            'endHour': forms.DateTimeInput(attrs={
                'class': 'form-control datetimepicker-input',
                'data-target': '#datetimepicker1'
            })
        }
