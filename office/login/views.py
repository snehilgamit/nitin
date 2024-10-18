from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


# def login(request):
#     return render(request,'login.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # User is authenticated
            data = login(request, user)
            # Redirect to a success page or home page
            return redirect('home')
        else:
            # Authentication failed
            return render(request, 'login.html', {'error': 'Invalid username or password'})

    return render(request, 'login.html')


def registration(request):
    error="Registration is done only Through staff Member "
    return render(request, 'login.html', {'error': error})

def forgot_password(request):
    error="Password reset can done only through Admim "
    return render(request, 'login.html', {'error': error})

from django.shortcuts import redirect
from django.contrib.auth import logout

def my_logout_view(request):
    logout(request)
    return redirect('home')