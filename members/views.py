from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .form import RegisterUserForm, UserForm, UserFormUpdate, UserProfileUpdate, UserPasswordUpdate, UserRoleForm
from django.contrib.auth.decorators import login_required
# Create your views here.
from members.models import UserProfile

# Logic behind the login page
def login_user(request):
    # If we request to take details from the template, when user presses Log In
    if request.method == "POST":
        username = request.POST['username']     # username typed by user in the box input
        password = request.POST['password']     # password typed by user in the box input
        user = authenticate(request, username=username, password=password)
        # If user exist in the database
        if user is not None:
            user = User.objects.get(pk=user.id)
            # If user has a User Role or is Admin
            if user.userprofile.title or user.is_superuser:
                login(request, user)
                messages.success(request, ("Welcome back " + user.first_name ))
                return redirect('home')  # Redirect to a Home page.
            # if used hasn't been assigned a User Role
            else:
                messages.success(request, ("Contact staff, you need to be given a role in order to use the site" ))
                return redirect('login')  # Redirect to a Login page.
        # If there was another error in the form, like wrong credentials.
        else:
            messages.success(request,("There was an error trying to log in, try again"))
            return redirect('login-again', username)  # Redirect to a success page.
    # Request to load the login page
    else:
        return render(request, 'authenticate/login.html', {})

# Logging out
@login_required # user must be authenticated to reach that function
def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out Successfully"))
    return redirect('login')

# Logic behind Registration of new users
@login_required
def register_user(request):
    # assign RegistrationUserForm
    form = RegisterUserForm(request.POST)
    # If we request to Post and receive data from template
    if request.method == "POST":
        # If form is valid without errors on input
        if form.is_valid():
            form.save()     #save the form
            # set username as the typed username
            username = form.cleaned_data['username']
            # set password as password1 typed, which is same as password2
            password = form.cleaned_data['password1']
            # Log in the user
            user = authenticate(username=username,password=password)
            # Create a User Profile for that new user
            new_profile, created = UserProfile.objects.get_or_create(user=user)
            # pop a notification message on screen
            messages.success(request,("Registration successful. Don't forget to give the user a role."))
            # redirect to User Role, to assign new user a role
            return redirect('user-info', user.id)
        # If form isn't valid, maybe cause of wrong typed password etc
        else:
            messages.success(request, ("Registration failed, be sure to follow the password requirements"))
            form = RegisterUserForm
    # render register_user template and pass the form there.
    return render(request, 'authenticate/register_user.html', {'form': form})

# User List dashboard for the administrator, with diff options to change details of users.
@login_required
def user_list(request):
    # Load all user objects except administrator
    users = User.objects.all().exclude(is_superuser=True)
    # Create paginator for every 5 entries, ordered by id and pass userPerPge to the template.
    p = Paginator(users.order_by('-id'), 5)
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)
    return render(request, 'authenticate/user_list.html', {'users': usersPerPage})

# Admin view of User Profile, to assign a role toa  new user
@login_required
def user_info(request, user_id):
    # Select one specific user with that user_id
    userSelected = User.objects.get(pk=user_id)
    # Select his user Profile
    userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
    form = UserForm(request.POST or None, instance=userSelected)    #UserForms contain user role and user phone
    if form.is_valid():
        form.save()
        messages.success(request, "Profile has been updated")
        return redirect('user-list')

    return render(request, 'authenticate/user_info.html', {'user': userSelected, 'form': form})

# Admin view of User Role, where he can update a role of a user.
@login_required
def user_role(request, user_id):
    # Select the user with id==user_id, and then select his User Profile
    userSelected = User.objects.get(pk=user_id)
    userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
    form = UserRoleForm(request.POST or None, instance=userSelected)
    if form.is_valid():
        # save his new user role
        form.save()
        messages.success(request, "Profile has been updated")
        return redirect('user-list')

    return render(request, 'authenticate/user_role.html', {'user': userSelected, 'form': form})

# User's view of update profile
@login_required
def user_profile(request, user_id):
    userid = User.objects.get(pk=user_id)
    # if active user owns the profile or the user is admin, the has access to the profile
    if request.user == userid or request.user.is_superuser:
        # select the profile
        userSelected, created = UserProfile.objects.get_or_create(user=userid)
        # load the data to the form for Profile Update view
        form = UserProfileUpdate(request.POST or None, instance=userid)
        profileForm = UserFormUpdate(request.POST or None, instance=userSelected)
        if request.method == "POST":
            if form.is_valid():
                user = form.save()
                if profileForm.is_valid():
                    profileForm.save()
                    messages.success(request, ("Profile updated successfully"))
                else:
                    messages.success(request, ("userForm isn't valid"))
            else:
                messages.success(request, ("form isn't valid"))
            # Redirect user based on if the user is Student or Admin
            if request.user.is_superuser:
                return redirect('user-list')
            else:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('user-profile', user_id)
    else:
        messages.success(request, "You don't have permission to view other users informations")
        return redirect('home')

    return render(request, 'authenticate/user_profile.html', {'form': form, 'profileForm': profileForm, 'userid': userid})

@login_required
def user_password(request,user_id):
    userid = User.objects.get(pk=user_id)
    if request.user == userid or request.user.is_superuser:
        form = UserPasswordUpdate(request.POST or None, instance=userid)
        if request.method == "POST":
            if form.is_valid():
                user = form.save()
                messages.success(request, ("Password updated successfully"))
            else:
                messages.success(request, ("There was a mistake, please try again after reading the password requirements."))
                return redirect('user-password', user_id)
            # Redirect user based on if the user is Student or Admin
            if request.user.is_superuser:
                return redirect('user-list')
            else:
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('user-profile', user_id)
    else:
        messages.success(request, "You don't have permission to visit that page")
        return redirect('home')
    return render(request, 'authenticate/user_password.html', {'form': form, 'userid': userid})

# A quick way to keep the same username on input if a user fail to write password correctly
def login_user_again(request, username):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user = User.objects.get(pk=user.id)
            if user.userprofile.title or user.is_superuser:
                login(request, user)
                messages.success(request, ("Welcome back " + user.first_name ))
                return redirect('home')  # Redirect to a success page.
            else:
                messages.success(request, ("Contact staff, you need to be given a role in order to use the site" ))
                return redirect('login')  # Redirect to a success page.
        else:
            messages.success(request,("There was an error trying to log in, try again"))
            return redirect('login-again', username)  # Redirect to a success page.
    else:
        return render(request, 'authenticate/login-again.html', {"username":username})
