from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import User, Accounts, ATMcards, Transactions,Banks
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.http import JsonResponse


services = [
        {"name": "Bill Payments", "url": "billpayment", "icon": "bi-broadcast", "description": ""},
        {"name": "Card Detail", "url": "carddetail", "icon": "bi-broadcast", "description": ""},
        {"name": "Fund Transfer", "url": "fundtransfer", "icon": "bi-broadcast", "description": ""},
        {"name": "Account Info", "url": "accountInfo", "icon": "bi-broadcast", "description": ""},
        {"name": "Transaction Details", "url": "transactionDetails", "icon": "bi-broadcast", "description": ""},
        {"name": "Account Statement", "url": "statement", "icon": "bi-broadcast", "description": ""},        
    ]

def login(request):
    if 'user' in request.session:
        del request.session['user']
        
    if request.method == 'POST':
    # Ensure that the 'Username_signup' field is provided in the POST request
        if request.POST.get('Username_signup') and request.POST.get('Account_no'):
            # Attempt to retrieve the account using the account number provided in the POST request
            try:
                acc = Accounts.objects.get(account_number=request.POST.get('Account_no'))
                user = User.objects.get(id=acc.user_id)
                
                user.username = request.POST.get('Username_signup')
                user.password = request.POST.get('Password_signup1')
                user.save()
                
                # If successful, display a success message and redirect to the login page
                messages.success(request, 'Account created successfully, please log in.')
                return redirect('login')
            
            except ObjectDoesNotExist:
                # If the account number does not exist, display an error message
                messages.error(request, 'Incorrect Account No or CNIC')  # Use messages.error for errors
                return redirect('signup')  # It might be more appropriate to redirect back to signup
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
    return render(request, 'dashboard/carddetail.html',{'card': card, 'account': account,'services': services,'user': user})

from django.http import JsonResponse

def fundtransfer(request):
    banks = Banks.objects.all()
    if request.method == 'POST':
        account_number = request.POST.get('account_number')
        amount = request.POST.get('amount')
        bank_id = request.POST.get('bank')
        user = User.objects.get(id=request.session.get('user'))
        account = Accounts.objects.get(user_id=user)

        if account.balance < float(amount):
            return JsonResponse({'status': 'error', 'message': 'Insufficient balance.'}, status=400)
        
        if Accounts.objects.filter(account_number=account_number).exists() and account_number != account.account_number:
            reciver = Accounts.objects.get(account_number=account_number)
            account.balance -= float(amount)
            account.save()
            trans_debit = Transactions(
                amount=float(amount),
                transaction_type='debit',
                description='Funds transferred to account number ' + account_number,
                user_id=user.id
            )
            trans_debit.save()

            if bank_id == '11':  # Assuming '11' is the ID for intra-bank transfers
                reciver.balance += float(amount)
                reciver.save()
                trans_credit = Transactions(
                    amount=float(amount),
                    transaction_type='credit',
                    description='Funds received from account number ' + account.account_number,
                    user_id=reciver.user_id 
                )
                trans_credit.save()

            return JsonResponse({'status': 'success', 'message': 'Funds transferred successfully.'})
        
    return render(request, 'dashboard/fundtransfer.html', {'banks': banks, 'services': services})



def about(request):
    return render(request, 'dashboard/about.html')

def accountInfo(request):
    user_id = request.session.get('user')  # Make sure this session key is correct
    user = get_object_or_404(User, pk=user_id)
    account = get_object_or_404(Accounts, user_id=user)  # Use user instance here
    card = get_object_or_404(ATMcards, accounts_id=account)  # Use account instance here
    print(user,account,card)
    print(card.expiry_date)
    return render(request,'dashboard/accountInfo.html',{'User' : user, 'Account' : account,'ATMcards': card, 'services': services})

def transactionDetails(request):
    user_id=request.session.get('user')
    user=get_object_or_404(User,pk=user_id)
    transactions = Transactions.objects.filter(user_id=user,transaction_type='debit') 
    print(transactions)
    return render(request, 'dashboard/transactionDetails.html',{'transactions': transactions,'services' : services,'User':user})

def statement(request):
    user_id=request.session.get('user')
    user=get_object_or_404(User,pk=user_id)
    transactions = Transactions.objects.filter(user_id=user) 
    return render(request, 'dashboard/statement.html',{'transactions': transactions,'services' : services,'User':user}) 