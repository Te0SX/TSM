from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from .form import RegisterUserForm, UserForm
# Create your views here.
from members.models import UserProfile, UserRoles


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Welcome back " + username))
            return redirect('home')             # Redirect to a success page.
        else:
            messages.success(request,("There was an error login in, try again"))
            return redirect('login')  # Redirect to a success page.
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Logout successfully"))
    return redirect('home')

def user_list(request):
    users = User.objects.all()
    p = Paginator(users.order_by('id'), 5)  # filter User's shifts only
    page = request.GET.get('page')
    usersPerPage = p.get_page(page)
    return render(request, 'authenticate/user_list.html', {'users': usersPerPage})

def user_info(request, user_id):
    userSelected = User.objects.get(pk=user_id)
    userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
    form = UserForm(request.POST or None, instance=userSelected)
    if form.is_valid():
        form.save()
        userSelected.save()
        messages.success(request, "User has been promoted")
        return redirect('user-list')


    return render(request, 'authenticate/user_info.html', {'user': userSelected, 'form': form})

def register_user(request):
    form = RegisterUserForm(request.POST)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            new_profile, created = UserProfile.objects.get_or_create(user=user)
            messages.success(request,("Registration successful."))
            return redirect('user-info', user.id)

        else:
            form = RegisterUserForm

    return render(request, 'authenticate/register_user.html', {'form':form})


def user_profile(request, user_id):
    userSelected = User.objects.get(pk=user_id)
    form = UserForm(request.POST or None, instance=userSelected)
    if request.method == "POST":
        email = request.POST['email']
        # password = request.POST['password']
        if form.is_valid():
            userSelected.save()
            form.save()
    return render(request, 'authenticate/user_profile.html', {'form': form})