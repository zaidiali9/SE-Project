from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User
from django.contrib.auth.hashers import make_password, check_password

def login(request):
    if request.method == 'POST':
        if request.POST.get('Username_signup'):
            # Create and save a new user
            user = User()
            user.name = request.POST.get('FullName')
            user.email = request.POST.get('Email_signup')
            user.password = make_password(request.POST.get('Password_signup1'))
            user.address = request.POST.get('Address')
            user.CNIC = request.POST.get('CNIC')
            user.phone = request.POST.get('Ph_no')
            user.save()
            messages.success(request, 'Account created successfully, please log in.')
            return redirect('login')  # Use the name of your login route
        else:
            uname = request.POST.get('Username_signin')
            pword = request.POST.get('Password_signin')
            try:
                user = User.objects.get(name=uname)
                if (pword == user.password):
                    print("User is successfully logged in.")
                    messages.success(request, "User is successfully logged in.")
                else:
                    print("Invalid login credentials.")
                    messages.error(request, "Invalid login credentials.")
            except User.DoesNotExist:
                print("User does not exist.")
                messages.error(request, "User does not exist.")
            return redirect('login')  # Use the name of your login route

    return render(request, 'authentication/index.html')
