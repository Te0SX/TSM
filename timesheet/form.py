from django import forms
from django.forms import ModelForm, DateInput
from .models import Shift, Message
from tempus_dominus.widgets import DateTimePicker
from django.contrib.auth.models import User


# Create a Shift form

class ShiftForm(ModelForm):

    class Meta:
        model = Shift
        exclude = ['studentID']         # Will be taken from the request
        fields = ('role', 'startHour','endHour')
        labels = {
            'startHour': 'Start of Shift',
            'endHour': 'End of Shift',
            }
        widgets = {
            # 'studentID': forms.Select(attrs={'class':'form-select'}),
            'role': forms.Select(attrs={'class':'form-select'}),
            'startHour': DateTimePicker(attrs={
                    'data-target': '#datetimepicker1',
                }),
            'endHour': DateTimePicker(attrs={
                'data-target': '#datetimepicker2'
            })
        }

class MessageForm(ModelForm):

    class Meta:
        model = Message
        exclude = ['sender', 'receiver','sender_role', 'msg_title', 'msg_content']
        field = ()

