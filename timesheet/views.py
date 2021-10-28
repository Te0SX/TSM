from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect

from .models import Shift, Timesheet, Roles
from .form import ShiftForm

# Create your views here.
def home(request):
    name = "John"

    #Get current year
    now = datetime.now()
    current_year = now.year
    month = now.month

    # create a calendar
    cal = HTMLCalendar().formatmonth(current_year,month)

    #Get current time
    time = now.strftime('%H:%M')       #https://docs.python.org/3/library/datetime.html

    return render(request, 'timesheet/home.html', {
        "name": name,
        "year": current_year,
        "cal": cal,
        "current_year": current_year,
        "time": time,
    })

def all_timesheets(request):
    timesheet_list = Timesheet.objects.all()
    shift = Shift.objects.first()
    payment = shift.payment

    return render(request, 'timesheet/timesheet_list.html',
                  {'timesheet_list': timesheet_list,
                   'payment': payment})

def add_shift(request):

    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_shift')
    else:
        form = ShiftForm


    return render(request, 'timesheet/add_shift.html', {'form':form})