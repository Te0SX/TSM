import datetime

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

    def __str__(self):
        return str(self.studentID)

class Salary(models.Model):
    studentID = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateTimeField('Date added', auto_now_add=True)
    amount = models.IntegerField('Amount paid', default=0)

    def __int__(self):
        return self.amount
