from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
import csv

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
    p = Paginator(Shift.objects.filter(studentID=userid).order_by('-date'),4)   #filter User's shifts only
    page = request.GET.get('page')
    shiftsPerPage = p.get_page(page)

    return render(request, 'timesheet/shifts.html', {
        'shifts': shifts,
        'shiftsPerPage': shiftsPerPage,
        })

def all_shifts(request):
    shifts = Shift.objects.all().order_by('-date')
    userTitle = str(request.user.userprofile.title)

    # Paginator setup
    p = Paginator(shifts, 15)  # filter User's shifts only
    page = request.GET.get('page')
    shiftsPerPage = p.get_page(page)
    return render(request, 'timesheet/all_shifts.html',
              {'shifts': shifts,
               'shiftPerPage': shiftsPerPage})


def verified_shifts(request):
    shifts = Shift.objects.all().order_by('-date')

    return render(request, 'timesheet/verified_shifts.html', {'shifts': shifts})

def add_shift(request):
    # TODO add requirementfor user to be Student
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
    if request.user == shift.studentID:
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
        'form': form})

    else:
        messages.success(request, "You don't have permission to modify #" + shift_id +". Don't be sneaky!!!")
        return redirect('shifts')


def delete_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if request.user == shift.studentID:
        shift.delete()
        messages.success(request, "Shift #" + shift_id +" deleted successfully")
    else:
        messages.success(request, "You don't have permission to delete #" + shift_id +". Don't be sneaky!!!")

    return redirect('shifts')

def verify_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    isAdmin = request.user.is_superuser # If user is Admin, True
    if userTitle == 'Verifier':
        if shift.verified and shift.paid is False:
            shift.verified = False
            shift.save()
            messages.success(request, "Shift #" + shift_id + " has been unverified")
        elif shift.verified and shift.paid is True:
            messages.success(request, "Shift #" + shift_id + " has been paid and can't be unverified")
        else:
            shift.verified = True
            shift.save()
            messages.success(request, "Shift #" +shift_id +" has been verified")
        return redirect('all-shifts')
    elif userTitle == 'Payer' or isAdmin:
        messages.success(request, "You don't have the permission to verify shifts")
        return redirect('all-shifts')
    else:
        messages.success(request, "You don't have the permission to verify shifts")
        return redirect('shifts')

def pay_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    isAdmin = request.user.is_superuser # If user is Admin, True
    if userTitle == 'Payer':
        if shift.verified:
            shift.paid = True
            shift.save()
            messages.success(request, "Shift #" + shift_id + " has been paid")
            return redirect('all-shifts')
        else:
            messages.success(request, "Shift #" + shift_id + " hasn't been verified yet and can't be paid")
            return redirect('all-shifts')
    elif userTitle == 'Verifier' or isAdmin:
        messages.success(request, "You don't have the permission to verify payments")
        return redirect('all-shifts')
    else:
        messages.success(request, "You don't have the permission to verify payments")
        return redirect('shifts')

def warning(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if shift.verified:
        messages.success(request, "Shift #" + shift_id + " has been verified and can't be modified anymore")

def shifts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=shifts.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    userid = request.user.id
    shifts = Shift.objects.filter(studentID=userid).order_by('-date')

    # Add column heading to the csv file
    writer.writerow(['ShiftID', 'Date Added', 'Role', 'Start of Shift', 'Finish of Shift', 'Amount', 'Verified', 'Paid'])

    #Loop through and output
    for shift in shifts:
        writer.writerow([shift.id, shift.date, shift.role, shift.startHour, shift.endHour, shift.payment(), shift.verified, shift.paid])

    return response

