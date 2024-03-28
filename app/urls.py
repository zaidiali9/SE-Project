from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name="login"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('billpayment/', views.billpayment, name='billpayment'), 
    path('card/', views.card, name='carddetail'),
    path('fundtransfer/', views.fundtransfer, name='fundtransfer'),
]
