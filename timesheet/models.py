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

class Student(models.Model):
    firstName = models.CharField('First Name',  max_length=120)
    lastName = models.CharField('Last Name',  max_length=120)
    studentID = models.IntegerField('ID of student')
    email = models.EmailField('Email of student')
    telephone = models.IntegerField('Phone Number', null=True, blank=True)

    def __str__(self):
        return self.firstName + ' ' + self.lastName

class Shift(models.Model):
    # studentID = models.ForeignKey(Student, blank=True, null=True, on_delete=models.CASCADE)
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

class Timesheet(models.Model):
    name = models.CharField('Name of Timesheet',  max_length=120)
    year = models.DateTimeField('Year of Timesheet')
    shifts = models.ManyToManyField(Shift, blank=True)

    def __str__(self):
        return self.name