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
            return redirect('login')  
        else:
            uname = request.POST.get('Username_signin')
            pword = request.POST.get('Password_signin')
            try:
                user = User.objects.get(name=uname)
                if (pword == user.password):  
                    request.session['user'] = user.id  
                    return redirect('dashboard') 
                else:
                    messages.error(request, "Invalid login credentials.")
            except User.DoesNotExist:
                messages.error(request, "User does not exist.")
            return redirect('login')  

    return render(request, 'authentication/index.html')



def dashboard(request):
    services = [
        {"name": "Bill Payments", "url": "Billpayments.aspx", "icon": "bi-broadcast", "description": ""},
        {"name": "Donations", "url": "donations.aspx", "icon": "bi-broadcast", "description": ""},
        {"name": "Transactions", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Card Details", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "User Profile", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Mobile Topup", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Loans", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Traveling", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Investments", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Cheques", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Budget Planner", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Foreign Currency", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Analytics", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Money Transfer", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Educational Institutes", "url": "", "icon": "bi-broadcast", "description": ""},
        {"name": "Transaction History / Loan History", "url": "", "icon": "bi-broadcast", "description": ""},
        
        # Add more services as needed
    ]
    if 'user' in request.session: 
        return render(request, 'dashboard/index.html' ,{'services': services})
    else:
        messages.error(request, "You must be logged in to view the dashboard.")
        return redirect('login')  
