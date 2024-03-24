from django.shortcuts import render

# Create your views here.
rooms = [
    {'id': 1, 'name': 'Lets learn python!'},
    {'id': 2, 'name': 'Design with me'},
    {'id': 3, 'name': 'Frontend developers'},
]


def login(request):
    if request.method == 'POST':
    
    return render(request, 'authentication/index.html')

def room(request):
    return render(request, 'app/room.html')