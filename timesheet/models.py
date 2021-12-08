import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Roles(models.Model):
    name = models.CharField('Type of role', max_length=120)
    hourlyPay = models.IntegerField('Payment per hour for a role')

    def hourlyPayment(self):
        return self.hourlyPay

    def __str__(self):
        return self.name


class Shift(models.Model):
    studentID = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField('Date added', auto_now_add=True)
    role = models.ForeignKey(Roles, null=True, on_delete=models.SET_NULL)
    startHour = models.DateTimeField('Time started working')
    endHour = models.DateTimeField('Time finished working')
    verified = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    def payment(self):
        time = self.endHour - self.startHour                                 #calculate time working
        payment = round(self.role.hourlyPay * time.seconds / 60 / 60,2)      #hourlyPay * hours worked, rounded for 2 demicals
        return payment

    def clean(self, *args, **kwargs):
        if self.startHour > self.endHour :
            raise ValidationError('Start of the Shift is not earlier than the End of the Shift')
        return super().clean(*args, **kwargs)

    def __str__(self):
        return str(self.studentID)

class Salary(models.Model):
    studentID = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField('Date added', auto_now_add=True)
    amount = models.FloatField('Amount paid', default=0)

    def __int__(self):
        return self.amount

class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)
    msg_title = models.CharField("Title", max_length=50)
    msg_content = models.CharField("Content of message", max_length=3000)
    sender_role = models.CharField("Role of Sender", max_length=50)
    date = models.DateTimeField('Date added', auto_now_add=True)
    read = models.BooleanField(default=False)
    resolved =  models.BooleanField(default=False)

    def __str__(self):
        return str(self.receiver)