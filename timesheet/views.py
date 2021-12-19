# ------------------ Theodoros Vrakas -------------- #
# -------------------------------------------------- #
# ------------------ Import modules ---------------- #
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.http import HttpResponseRedirect, HttpResponse
import csv

from .models import Shift, Salary, Message
from .form import ShiftForm, MessageForm
from members.models import UserProfile

from django.core.paginator import Paginator

# -------------------------------------------------- #
# ------------------ Main Body --------------------- #

def home(request):
    return render(request, 'timesheet/home.html', {})

def about(request):
    return render(request, 'timesheet/about.html', {})

def support(request):
    return render(request, 'timesheet/support.html', {})

# Logic behind appearance of shifts in their dashboard.
@login_required
def shifts(request):
    # Take all shifts and order then by date
    shifts = Shift.objects.all().order_by('-date')
    # load authenticated user's role as a string
    userTitle = str(request.user.userprofile.title)
    # If user is Student, create his view, the table formed on the template will have 5 entries per page
    if userTitle == 'Student':
        userid = request.user.id
        #Paginator setup, filters the shifts and take only the one owned by the specific student
        p = Paginator(Shift.objects.filter(studentID=userid).order_by('-date'),5)   #filter User's shifts only
        page = request.GET.get('page')
        shiftsPerPage = p.get_page(page)

        return render(request, 'timesheet/shifts.html', {
            'shiftsPerPage': shiftsPerPage,
            })
    # if authenticated user is staff, returns all the shifts, 10 per page, renders All Shifts html
    else:
        p = Paginator(shifts, 10)  # filter User's shifts only
        page = request.GET.get('page')
        shiftsPerPage = p.get_page(page)

        return render(request, 'timesheet/all_shifts.html', {
            'shiftsPerPage': shiftsPerPage
            })

# Logic of shifts view per student, when a Staff view their timesheet from their dashboard
@login_required
def shifts_of(request, user_id):
    userid = User.objects.get(pk=user_id)
    # Take all the shifts of specific student with id == user_id
    shifts = Shift.objects.filter(studentID=user_id).order_by('-date')
    # load authenticated user's role as a string
    userTitle = str(request.user.userprofile.title)
    # Only Verifier and Staff can access others' timesheet
    if userTitle == 'Verifier' or userTitle == 'Admin':
        # Notification for Verifier, turns to False when he enters someone's updated timesheet
        if userTitle == 'Verifier':
            userSelected, created = UserProfile.objects.get_or_create(user=userid)
            userSelected.addedToTimesheet = False
            userSelected.save()
        # Paginator setup, 5 entries per page
        p = Paginator(shifts, 5)
        page = request.GET.get('page')
        shiftsPerPage = p.get_page(page)
        # renders shifts_of and passes shiftsPerPage and user to template to create the layout there
        return render(request, 'timesheet/shifts_of.html', {
            'shiftsPerPage': shiftsPerPage,
            'user': userid,
        })
    # if someone tries to sneak into someone's else timesheet
    else:
        messages.success(request, "You don't have permissions to view this page. Gtfo.")
        return redirect('shifts')

# Add a shift to the timesheet, only for students
@login_required
def add_shift(request):
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    form = ShiftForm(request.POST)
    # If authenticated user is a students
    if userTitle == 'Student':
        # If request to post a new shift
        if request.method == 'POST':
            if form.is_valid():
                # form is set to currentShifts but is not saved yet
                currentShift = form.save(commit=False)
                # save studentID as the authenticated user who add this shift, so user doesn't have to type his username
                currentShift.studentID = request.user       # Save the studentID instantly without input in the form
                # Now save the form
                currentShift.save()
                messages.success(request, "Shift was added successfully.")
                # Notification for Verifier to True, for this specific user's timesheet new entry
                userSelected, created = UserProfile.objects.get_or_create(user=request.user)
                userSelected.addedToTimesheet = True
                userSelected.save()
                return HttpResponseRedirect('shifts')
            else:
                messages.success(request, "Start of the Shift is not earlier than the End of the Shift. Try again.")
                return HttpResponseRedirect('add_shift')
        # If request to just load form for this page
        else:
            form = ShiftForm
        # render the add_shift and pass the form
        return render(request, 'timesheet/add_shift.html', {'form': form})
    # if someone else tries to add a shift to someone's else timesheet
    else:
        messages.success(request, "You don't have permissions to add a shift")
        return redirect('shifts')

# Update an submitted shift, for potential mistakes.
@login_required
def update_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    # if user is the same as the guy who entered that shift
    if request.user == shift.studentID:
        # if shift has been verified, you can modify it
        if shift.verified:
            messages.success(request, "Shift #" + shift_id + " has been already verified and can't be modified anymore")
            return redirect('shifts')
        # otherwise you can modify it
        else:
            form = ShiftForm(request.POST or None, instance=shift)
            if form.is_valid():
                form.save()
                messages.success(request,"Shift #" +shift_id +" updated successfully")
                return redirect('shifts')

        return render(request, 'timesheet/update_shift.html', {
                'shift': shift,
                'form': form})
    # if it's someone else shift, you can't modify it
    else:
        messages.success(request, "You don't have permission to modify #" + shift_id +". Don't be sneaky!!!")
        return redirect('shifts')

# Delete a shift
@login_required
def delete_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    # if user is the same as the guy who entered that shift
    if request.user == shift.studentID:
        shift.delete()
        messages.success(request, "Shift #" + shift_id +" deleted successfully")
    else:
        messages.success(request, "You don't have permission to delete #" + shift_id +". Don't be sneaky!!!")

    return redirect('shifts')

# Verify a shift, only for verifier role
@login_required
def verify_shift(request, shift_id):
    # Choose specific shift from timesheet with that shift id
    shift = Shift.objects.get(pk=shift_id)
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    isAdmin = request.user.is_superuser # If user is Admin, True
    ownerID = shift.studentID           # studentID of the owner
    salary = ownerID.userprofile.salary # current remaining amount of the student who owns that shift
    # if authenticated user is Verifier
    if userTitle == 'Verifier':
        # if shift has been Verified but has NOT been paid
        if shift.verified and shift.paid is False:
            # turn verified to false, since it turns to unverified
            shift.verified = False
            shift.save()
            # remove the shift's amount from the current remaining salary amount
            salary -= shift.payment()
            ownerID.userprofile.salary = round(salary,2)    # round the number with 2 demicals
            ownerID.userprofile.save()                      # save the amount to student profile

            messages.success(request, "Shift #" + shift_id + " has been unverified")
        # if shift has been verified AND has been paid
        elif shift.verified and shift.paid is True:
            # now it can't be unverified anymore
            messages.success(request, "Shift #" + shift_id + " has been paid and can't be unverified")
        # if shift hasn't been verified
        else:
            # verified to True
            shift.verified = True
            shift.save()
            # add the shift's amount to the student remaining amount to be paid
            salary += shift.payment()
            ownerID.userprofile.salary = round(salary,2)     # round the number with 2 demicals
            ownerID.userprofile.save()                       # save the amount to student profile

            messages.success(request, "Shift #" +shift_id +" has been verified")
        return redirect('shifts-of', shift.studentID.id)
    # None except Verifier ca verify shifts
    elif userTitle == 'Payer' or isAdmin:
        messages.success(request, "You don't have the permission to verify shifts")
        return redirect('home')
    # None except Verifier ca verify shifts
    else:
        messages.success(request, "You don't have the permission to verify shifts")
        return redirect('shifts')

# Pay the remaining amount to the student only for that Shift, for Payer.
# That feature was replaced by Pay Salary, paying all submitted shifts of a student with one button.
@login_required
def pay_shift(request, shift_id):
    shift = Shift.objects.get(pk=shift_id)
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    isAdmin = request.user.is_superuser # If user is Admin, True
    # if user is Payer
    if userTitle == 'Payer':
        # If shift has been verified, only then can be paid
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

# Export the log of submitted shifts in csv format
@login_required
def shifts_csv(request):
    response = HttpResponse(content_type='text/csv')
    # name of the file that will be downloaded
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

# Export the log of paid salaries in csv format
@login_required
def salaries_csv(request):
    response = HttpResponse(content_type='text/csv')
    # name of the file that will be downloaded
    response['Content-Disposition'] = 'attachment; filename=salaries.csv'

    # Create a csv writer
    writer = csv.writer(response)

    # Designate the Model
    userid = request.user.id
    userTitle = str(request.user.userprofile.title) # Without str, it's a Role object, gives an error
    if userTitle == 'Student':
        salaries = Salary.objects.filter(studentID=userid).order_by('-date')
        # Add column heading to the csv file
        writer.writerow(['SalaryID', 'Date Paid', 'Amount'])
        # Loop through and output
        for salary in salaries:
            writer.writerow(
                [salary.id, salary.date, salary.amount])

    return response

# Paid Salary object, for the Salary dashboard logic for the student, and Admin only
@login_required
def salary(request, user_id):
    # Choose the student that has id == user_id
    user = User.objects.get(pk=user_id)
    # authenticated user role
    userTitle = str(request.user.userprofile.title)
    # if authenticated user is the student himself with that id or an Administrator
    if request.user == user or userTitle == "Admin":
        # filter and take all the salaries of that student
        salaries = Salary.objects.filter(studentID=user).order_by('-date')
        #Paginator for Paid Salaries, to show only # number per page
        p = Paginator(salaries, 5)  # filter User's shifts only
        page = request.GET.get('page')
        salariesPerPage = p.get_page(page)

        return render(request, 'timesheet/salary.html',{'salariesPerPage': salariesPerPage, 'user': user})
    else:
        messages.success(request, "You don't view the salary page for that person")
        return redirect('home')

# Pay all verified and unpaid shifts of one student with one click, like a monthly payment.
@login_required
def pay_salary(request, user_id):
    user = User.objects.get(pk=user_id)
    # take all verified and unpaid shifts of one student with that uder_id, order them by date
    shifts = Shift.objects.filter(studentID=user, verified=True, paid=False).order_by('-date')
    # authenticated user role
    userTitle = str(request.user.userprofile.title)

    if userTitle == 'Payer':
        # pay all the verified shifts
        for shift in shifts:
            shift.paid = True
            shift.save()

        #Add a new payment to paid salaries of user
        salary = Salary.objects.create()            # create a new payment
        salary.studentID = user                     # payment for that user with user_id
        salary.amount = user.userprofile.salary     # amount of payment equals to user's remaining amount to be paid
        salary.save()                               # save and submit payment

        user.userprofile.salary = 0                 # turn remaining amount of user to 0
        user.userprofile.save()                     # save remaining amount of that user
        messages.success(request, "Payment has been processed")
    else:
        messages.success(request, "You don't have permissions to pay salaries")

    return redirect('user-salary-list')

# Salary List Dashboard for the Payer, all users appear on a list in table view when can pay each with one click
@login_required
def user_salary_list(request):
    users = User.objects.all().exclude(is_superuser=True)   # all users except supervisor
    p = Paginator(users.order_by('-id'), 5)  # filter User's shifts only
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)

    return render(request, 'timesheet/user_salary_list.html', {'users': usersPerPage})

# Timsheets Dashboard for Verifier, list of users in table view
# where verifier and admin can enter each person timesheet separately
@login_required
def user_timesheets_list(request):
    users = User.objects.filter(userprofile__title=1) #Students
    p = Paginator(users.order_by('-id'), 10)  # filter User's shifts only
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)

    return render(request, 'timesheet/user_timesheets_list.html', {'users': usersPerPage})

# Send a message to a student Inbox, used by Verifier and Administrator
@login_required
def send_message(request, user_id, shift_id):
    # student with that user_id
    receiver = User.objects.get(pk=user_id)
    # select student's profile
    userSelected, created = UserProfile.objects.get_or_create(user=user_id)
    # sender's role, Verifier or Admin
    senderRole = str(request.user.userprofile.title)
    # Title of the message is auto-generated, including the problematic Shift submission that is about
    title =  str('Ticket for Shift #' + shift_id)
    form = MessageForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user                    # Save the sender instantly without input in the form
            message.receiver = receiver                      # Save the receiver
            message.msg_title = title                        # save the title
            message.sender_role = str(senderRole)            #save the role
            messages.success(request, "Message was sent successfully.")
            message.msg_content = request.POST['content']   # take typed message content from the template
            message.save()                                  # save and submit the message
            userSelected.inboxNotification = True           # set notification for the student to check the inbox
            userSelected.save()                             # save message

            return redirect('shifts-of', user_id)
        else:
            messages.success(request, "Message form wasn't filled successfully.")
            return redirect('home')
    else:
        form = MessageForm

    return render(request, 'timesheet/send_message.html', {'form': form, 'receiver': receiver, 'title': title})

# Read a message from the inbox
@login_required
def read_message(request, message_id):
    message = Message.objects.get(pk=message_id)
    form = MessageForm(instance=message)
    userTitle = str(request.user.userprofile.title)
    # if the message is opened by Student, turn the message.read notification to True, so it becomes black
    if userTitle == "Student":
        message.read = True
        message.save()

    return render(request, 'timesheet/read_message.html', {'form': form, 'message':message})

# Delete a message, for Verifier
@login_required
def delete_message(request, message_id):
    message = Message.objects.get(pk=message_id)
    userTitle = str(request.user.userprofile.title)
    # if user is verifier or Admin
    if userTitle == 'Verifier' or userTitle == 'Admin':
        message.delete()
        messages.success(request, "Message #" + message_id +" deleted successfully")
    else:
        messages.success(request, "You don't have permission to delete #" + message_id +". Don't be sneaky!!!")

    return redirect('inbox')

# Logic for Inbox dashboard
@login_required
def inbox(request):
    userTitle = str(request.user.userprofile.title)
    # These three users can see only their own messages in their inbox
    if userTitle == 'Student' or userTitle == 'Payer' or userTitle == 'Graduate':
        userid = request.user.id
        messages = Message.objects.filter(receiver=userid).order_by("-date")
    # if user is Admin or Verifier, they can view all messages sent to all students
    elif userTitle == 'Verifier' or userTitle == 'Admin':
        messages = Message.objects.all().order_by('-date')

    # Paginator setup
    p = Paginator(messages, 5)  # filter User's shifts only
    page = request.GET.get('page')
    messagesPerPage = p.get_page(page)

    # Turn off the notification for inbox icon for Verifier to change back to normal
    request.user.userprofile.inboxNotification = False
    request.user.userprofile.save()

    return render(request, 'timesheet/inbox.html', {'messagesPerPage': messagesPerPage})

@login_required
def resolve(request, message_id):
    message = Message.objects.get(pk=message_id)
    if request.user == message.receiver or request.user.is_superuser:
        # if issue hasn't resolved yet
        if message.resolved == False:
            # turn issue to resolved
            message.resolved = True
            message.save()
            sender = message.sender
            # Notification back to Verifier or Admin, who is the sender
            userSelected, created = UserProfile.objects.get_or_create(user=sender)
            userSelected.inboxNotification = True
            userSelected.save()

            messages.success(request, "Issue with Message #" + message_id + " resolved!")
        else:
            messages.success(request, "This issue has been already resolved. Wait for the Verifier to review it.")
    else:
        messages.success(request, "You have permission to resolve that issue.")

    return redirect('inbox')

