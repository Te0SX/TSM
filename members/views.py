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


def login_user(request):
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
            messages.success(request,("There was an error logging, try again"))
            return redirect('login')  # Redirect to a success page.
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out Successfully"))
    return redirect('login')

@login_required
def register_user(request):
    form = RegisterUserForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            new_profile, created = UserProfile.objects.get_or_create(user=user)
            messages.success(request,("Registration successful. Don't forget to give the user a role."))
            return redirect('user-info', user.id)

        else:
            messages.success(request, ("Registration failed, be sure to follow the password requirements"))
            form = RegisterUserForm

    return render(request, 'authenticate/register_user.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.all().exclude(is_superuser=True)
    p = Paginator(users.order_by('-id'), 5)  # filter User's shifts only
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)
    return render(request, 'authenticate/user_list.html', {'users': usersPerPage})

# Admin view of update profile
@login_required
def user_info(request, user_id):
    userSelected = User.objects.get(pk=user_id)
    userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
    form = UserForm(request.POST or None, instance=userSelected)
    if form.is_valid():
        form.save()
        userSelected.save()
        messages.success(request, "Profile has been updated")
        return redirect('user-list')

    return render(request, 'authenticate/user_info.html', {'user': userSelected, 'form': form})

@login_required
def user_role(request, user_id):
    userSelected = User.objects.get(pk=user_id)
    userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
    form = UserRoleForm(request.POST or None, instance=userSelected)
    if form.is_valid():
        form.save()
        userSelected.save()
        messages.success(request, "Profile has been updated")
        return redirect('user-list')

    return render(request, 'authenticate/user_role.html', {'user': userSelected, 'form': form})

# User's view of update profile
@login_required
def user_profile(request, user_id):
    userid = User.objects.get(pk=user_id)
    if request.user == userid or request.user.is_superuser:
        userSelected, created = UserProfile.objects.get_or_create(user=userid)
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
                messages.success(request, ("form isn't valid"))
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
