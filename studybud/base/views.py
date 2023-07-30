from django.shortcuts import render
from .models import Room

# Create your views here.
# rooms = [
#     {'id':1, 'name':'Python'},
#     {'id':2, 'name':'Web Development'},
#     {'id':3, 'name':'Data Science'},
# ]

def home(request):
    rooms = Room.objects.all()
    context = {'rooms':rooms}
    return render(request,'home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)

    context = {'room':room}
    return render(request,'room.html',context)