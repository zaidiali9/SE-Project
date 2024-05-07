from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('billpayment/', views.billpayment, name='billpayment'),
    path('card/', views.card, name='carddetail'),
    path('beneficiary/fundtransfer/', views.fundtransfer, name='fundtransfer'),
    path('about/', views.about, name='about'),
    path('accountInfo/', views.accountInfo, name="accountInfo"),
    path('transactionDetails/', views.transactionDetails, name="transactionDetails"),
    path('statement/', views.statement, name='statement'),
    path('beneficiary/', views.beneficiary, name='beneficiary'),
    path('beneficiary/addbeneficiary/', views.addbeneficiary, name='addbeneficiary'),
]
