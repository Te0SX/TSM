from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect

from .models import Shift, Timesheet, Roles
from .form import ShiftForm

#import Pegination stuff
from django.core.paginator import Paginator

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
    userid = request.user.id
    #Paginator setup
    p = Paginator(Shift.objects.filter(studentID=userid).order_by('-date'),4)
    page = request.GET.get('page')
    shiftsPerPage = p.get_page(page)

    return render(request, 'timesheet/shifts.html', {
        'shifts': shifts,
        'shiftsPerPage': shiftsPerPage,
        })

def verified_shifts(request):
    shifts = Shift.objects.all().order_by('-date')

    return render(request, 'timesheet/verified_shifts.html', {'shifts': shifts})

def add_shift(request):
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            currentShift = form.save(commit=False)
            currentShift.studentID = request.user       # Save the studentID instantly without input in the form
            currentShift.save()
            messages.success(request, "Shift added successfully")
            return HttpResponseRedirect('shifts')
    else:
        form = ShiftForm

    return render(request, 'timesheet/add_shift.html', {'form':form})

def update_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if shift.verified:
        messages.success(request, "Shift #" + shift_id + " has been already verified and can't be modified anymore")
        return redirect('shifts')
    else:
        form = ShiftForm(request.POST or None, instance=shift)
        if form.is_valid():
            form.save()
            messages.success(request,"Shift #" +shift_id +" updated successfully")

    return render(request, 'timesheet/update_shift.html', {
        'shift': shift,
        'form': form
    })



def delete_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    shift.delete()
    messages.success(request, "Shift #" +shift_id +" deleted successfully")

    return redirect('shifts')

def verify_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if shift.verified:
        shift.verified = False
        shift.save()
        messages.success(request, "Shift #" + shift_id + " has been already unverified")
    else:
        shift.verified = True
        shift.save()
        messages.success(request, "Shift #" +shift_id +" has been verified")

    return redirect('shifts')

def pay_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if shift.verified:
        shift.paid = True
        shift.save()
        messages.success(request, "Shift #" + shift_id + " has been paid")
    else:
        messages.success(request, "Shift #" + shift_id + " hasn't been verified yet and can't be paid")

    return redirect('shifts')

def warning(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if shift.verified:
        messages.success(request, "Shift #" + shift_id + " has been verified and can't be modified anymore")
