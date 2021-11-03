from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from members.form import userForm

# Create your views here.
from members.models import UserProfile


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

    return render(request, 'authenticate/user_list.html', {'users': users})

def user_info(request, user_id):
    userSelected = User.objects.get(pk=user_id)
    userSelected, created = UserProfile.objects.get_or_create(user=userSelected)
    form = userForm(request.POST or None, instance=userSelected)
    if form.is_valid():
        form.save()
        userSelected.save()
        messages.success(request, "User has been promoted")

    return render(request, 'authenticate/user_info.html', {'user': userSelected, 'form': form})
