from django.shortcuts import render

# Create your views here.

def login(request):
    return render(request, 'authentication/index.html')

def room(request):
    return render(request, 'app/room.html')