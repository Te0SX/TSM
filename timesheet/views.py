from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
import csv

from .models import Shift, Salary
from .form import ShiftForm

#import Pegination stuff
from django.core.paginator import Paginator

# Create your views here.
def home(request):
    return render(request, 'timesheet/home.html', {})

def about(request):
    return render(request, 'timesheet/about.html', {})

def support(request):
    return render(request, 'timesheet/support.html', {})

def warning(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if shift.verified:
        messages.success(request, "Shift #" + shift_id + " has been verified and can't be modified anymore")

@login_required
def shifts(request):
    shifts = Shift.objects.all().order_by('-date')
    userTitle = str(request.user.userprofile.title)
    #Students view
    if userTitle == 'Student':
        userid = request.user.id
        #Paginator setup
        p = Paginator(Shift.objects.filter(studentID=userid).order_by('-date'),4)   #filter User's shifts only
        page = request.GET.get('page')
        shiftsPerPage = p.get_page(page)

        return render(request, 'timesheet/shifts.html', {
            'shiftsPerPage': shiftsPerPage,
            })
    # Verifier & Payer view
    else:
        p = Paginator(shifts, 10)  # filter User's shifts only
        page = request.GET.get('page')
        shiftsPerPage = p.get_page(page)

        return render(request, 'timesheet/all_shifts.html', {
            'shiftsPerPage': shiftsPerPage
            })

@login_required
def verified_shifts(request):
    shifts = Shift.objects.all().order_by('-date')

    return render(request, 'timesheet/verified_shifts.html', {'shifts': shifts})

@login_required
def add_shift(request):
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    form = ShiftForm(request.POST)
    if userTitle == 'Student':
        if request.method == 'POST':
            if form.is_valid():
                currentShift = form.save(commit=False)
                currentShift.studentID = request.user       # Save the studentID instantly without input in the form
                currentShift.save()
                messages.success(request, "Shift added successfully")
                return HttpResponseRedirect('shifts')
            else:
                messages.success(request, "Start of the Shift is not earlier than the End of the Shift. Try again.")
                return HttpResponseRedirect('add_shift')
        else:
            form = ShiftForm

        return render(request, 'timesheet/add_shift.html', {'form': form})

    else:
        messages.success(request, "You don't have permissions to add a shift")
        return redirect('shifts')

@login_required
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
                return redirect('shifts')

        return render(request, 'timesheet/update_shift.html', {
                'shift': shift,
                'form': form})

    else:
        messages.success(request, "You don't have permission to modify #" + shift_id +". Don't be sneaky!!!")
        return redirect('shifts')

@login_required
def delete_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    if request.user == shift.studentID:
        shift.delete()
        messages.success(request, "Shift #" + shift_id +" deleted successfully")
    else:
        messages.success(request, "You don't have permission to delete #" + shift_id +". Don't be sneaky!!!")

    return redirect('shifts')

@login_required
def verify_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    isAdmin = request.user.is_superuser # If user is Admin, True

    ownerID = shift.studentID
    salary = ownerID.userprofile.salary

    if userTitle == 'Verifier':
        if shift.verified and shift.paid is False:
            shift.verified = False
            shift.save()

            salary -= shift.payment()
            ownerID.userprofile.salary = round(salary,2)
            ownerID.userprofile.save()

            messages.success(request, "Shift #" + shift_id + " has been unverified")
        elif shift.verified and shift.paid is True:
            messages.success(request, "Shift #" + shift_id + " has been paid and can't be unverified")
        else:
            shift.verified = True
            shift.save()

            salary += shift.payment()
            ownerID.userprofile.salary = round(salary,2)
            ownerID.userprofile.save()

            messages.success(request, "Shift #" +shift_id +" has been verified")
        return redirect('shifts-of', shift.studentID.id)
    elif userTitle == 'Payer' or isAdmin:
        messages.success(request, "You don't have the permission to verify shifts")
        return redirect('all-shifts')
    else:
        messages.success(request, "You don't have the permission to verify shifts")
        return redirect('shifts')

@login_required
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

@login_required
def shifts_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=shifts.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    userid = request.user.id
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    if userTitle == 'Student':
        shifts = Shift.objects.filter(studentID=userid).order_by('-date')
        # Add column heading to the csv file
        writer.writerow(['ShiftID', 'Date Added', 'Role', 'Start of Shift', 'Finish of Shift', 'Amount', 'Verified', 'Paid'])
        # Loop through and output
        for shift in shifts:
            writer.writerow(
                [shift.id, shift.date, shift.role, shift.startHour, shift.endHour, shift.payment(), shift.verified,shift.paid])
    else:
        shifts = Shift.objects.all().order_by('-date')
        writer.writerow(['ShiftID', 'StudentID', 'Date Added', 'Role', 'Start of Shift', 'Finish of Shift', 'Amount', 'Verified', 'Paid'])
        for shift in shifts:
            writer.writerow(
                [shift.id, shift.studentID, shift.date, shift.role, shift.startHour, shift.endHour, shift.payment(), shift.verified, shift.paid])

    return response

@login_required
def salary(request, user_id):
    user = User.objects.get(pk=user_id)

    shifts = Shift.objects.filter(studentID=user, verified=True, paid=False).order_by('-date')
    salaries = Salary.objects.filter(studentID=user).order_by('-date')

    #Paginator for Paid Salaries, to show only # number per page
    p = Paginator(salaries, 5)  # filter User's shifts only
    page = request.GET.get('page')
    salariesPerPage = p.get_page(page)

    return render(request, 'timesheet/salary.html',{'shifts': shifts, 'salary': salary, 'salariesPerPage': salariesPerPage})

@login_required
def pay_salary(request, user_id):
    user = User.objects.get(pk=user_id)
    shifts = Shift.objects.filter(studentID=user, verified=True, paid=False).order_by('-date')
    salary = Salary.objects.create()
    userTitle = str(request.user.userprofile.title)

    if userTitle == 'Payer':
        for shift in shifts:
            shift.paid = True
            shift.save()

        #Add a new payment to paid salaries of user
        salary.studentID = user
        salary.amount = user.userprofile.salary
        salary.save()

        user.userprofile.salary = 0
        user.userprofile.save()
        messages.success(request, "Payment has been processed")
    else:
        messages.success(request, "You don't have permissions to pay salaries")

    return redirect('user-salary-list')

@login_required
def user_salary_list(request):
    users = User.objects.all().exclude(is_superuser=True)
    p = Paginator(users.order_by('-id'), 5)  # filter User's shifts only
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)

    return render(request, 'timesheet/user_salary_list.html', {'users': usersPerPage})

@login_required
def user_timesheets_list(request):
    users = User.objects.filter(userprofile__title=1)
    p = Paginator(users.order_by('-id'), 10)  # filter User's shifts only
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)

    return render(request, 'timesheet/user_timesheets_list.html', {'users': usersPerPage})


@login_required
def shifts_of(request, user_id):
    userid = User.objects.get(pk=user_id)
    shifts = Shift.objects.filter(studentID=user_id).order_by('-date')
    userTitle = str(request.user.userprofile.title)
    # Students view
    if userTitle == 'Verifier' or userTitle == 'Admin':
        # Paginator setup
        p = Paginator(shifts, 4)  # filter User's shifts only
        page = request.GET.get('page')
        shiftsPerPage = p.get_page(page)

        return render(request, 'timesheet/shifts_of.html', {
            'shiftsPerPage': shiftsPerPage,
            'user': userid,
        })
    # if someone tries to sneak into someone's else timesheet
    else:
        messages.success(request, "You don't have permissions to view this page. Gtfo.")
        return redirect('shifts')