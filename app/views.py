from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import User, Accounts, ATMcards, Transactions,Banks
from django.contrib.auth.hashers import make_password, check_password



services = [
        {"name": "Bill Payments", "url": "billpayment", "icon": "bi-broadcast", "description": ""},
        {"name": "Card Detail", "url": "carddetail", "icon": "bi-broadcast", "description": ""},
        {"name": "Fund Transfer", "url": "fundtransfer", "icon": "bi-broadcast", "description": ""},
        
    ]

def login(request):
    if 'user' in request.session:
        del request.session['user']
        
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
                user = User.objects.get(username=uname)
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
    if 'user' in request.session: 
        return render(request, 'dashboard/index.html' ,{'services': services})
    else:
        messages.error(request, "You must be logged in to view the dashboard.")
        return redirect('login')  


def billpayment(request):
    bill_payment_options = [
        {"name": "Lahore Electric Supply Company (LESCO)", "identifier": "LESCO"},
        {"name": "Islamabad Electric Supply Company (IESCO)", "identifier": "IESCO"},
        {"name": "Gujranwala Electric Power Company (GEPCO)", "identifier": "GEPCO"},
        # Continue adding other options as needed
    ]
    return render(request, 'dashboard/billpayment.html', {'bill_payment_options': bill_payment_options,'services': services})


def card(request):
    user_id = request.session.get('user')  # Make sure this session key is correct
    user = get_object_or_404(User, pk=user_id)
    account = get_object_or_404(Accounts, user_id=user)  # Use user instance here
    card = get_object_or_404(ATMcards, accounts_id=account)  # Use account instance here
    return render(request, 'dashboard/carddetail.html',{'card': card, 'account': account,'services': services})

def fundtransfer(request):
    banks = Banks.objects.all()
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        print(account_number)
        amount = request.POST.get('amount')
        print(amount)
        bank_id = request.POST.get('bank')
        print(bank_id)
        type(bank_id)
        user = User.objects.get(id=request.session.get('user'))
        account = Accounts.objects.get(user_id=user)
        print(account) 
        if account.balance < float(amount):
            messages.error(request, "Insufficient balance.")
            return render(request, 'dashboard/fundtransfer.html', {'banks': banks, 'services': services})
        if Accounts.objects.get(account_number=account_number) and account_number != account.account_number:
            if bank_id=='11':
                print("Inside")
                reciver=Accounts.objects.get(account_number=account_number)
                print(reciver)
                account.balance -= float(amount)
                reciver.balance += float(amount)
                reciver.save()
            else:
                print("else")
                account.balance -= float(amount)

            account.save()
                
    return render(request, 'dashboard/fundtransfer.html', {'banks': banks, 'services': services})


def about(request):
    return render(request, 'dashboard/about.html')
