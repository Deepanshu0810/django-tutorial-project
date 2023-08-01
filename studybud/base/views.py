from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from .models import Room, Topic
from django.contrib.auth.models import User
from .forms import RoomForm

# Create your views here.
# rooms = [
#     {'id':1, 'name':'Python'},
#     {'id':2, 'name':'Web Development'},
#     {'id':3, 'name':'Data Science'},
# ]

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q)|
        Q(name__icontains=q)|
        Q(description__icontains=q)|
        Q(host__username__icontains=q)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'topics':topics, 'room_count':room_count}
    return render(request,'home.html',context)

def room(request,pk):
    room = Room.objects.get(id=pk)

    context = {'room':room}
    return render(request,'room.html',context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,'room_form.html',context)

def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    if request.method == 'POST':
        # for update, we need to pass the instance of the room
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form':form}
    return render(request,'room_form.html',context)

def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj':room}
    return render(request,'delete.html',context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except:
            # we will use django flash messages
            messages.error(request,'Username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username OR password is incorrect')

    context = {}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')