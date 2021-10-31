from django.shortcuts import render, redirect
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

def shifts(request):
    shifts = Shift.objects.all().order_by('-date')

    return render(request, 'timesheet/shifts.html',{'shifts': shifts})

def add_shift(request):

    if request.method == "POST":
        form = ShiftForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('shifts')
    else:
        form = ShiftForm

    return render(request, 'timesheet/add_shift.html', {'form':form})

def update_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    form = ShiftForm(request.POST or None, instance=shift)
    if form.is_valid():
        form.save()
        return redirect('shifts')

    return render(request, 'timesheet/update_shift.html', {
        'shift': shift,
        'form': form
    })

def delete_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    shift.delete()

    return redirect('shifts')