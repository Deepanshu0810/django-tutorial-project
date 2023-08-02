from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from .models import Room, Topic, Message
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
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method=='POST':
        msg_body = request.POST.get('msg_body')
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = msg_body
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id)
    
    context = {'room':room, 'room_messages':room_messages,'participants':participants}
    return render(request,'room.html',context)


@login_required(login_url='login')
def deleteMessage(request,pk):
    msg = Message.objects.get(id=pk)

    if request.user != msg.user:
        return HttpResponse('Permission Denied')
    
    if request.method == 'POST':
        msg.delete()
        return redirect('room',pk=msg.room.id)
    
    context = {'obj':msg}
    return render(request,'delete.html',context)

@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form =RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Permission Denied')

    if request.method == 'POST':
        # for update, we need to pass the instance of the room
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context ={'form':form}
    return render(request,'room_form.html',context)

@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Permission Denied')
    
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    context = {'obj':room}
    return render(request,'delete.html',context)

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        username = username.lower()
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

    context = {'page':page}
    return render(request,'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    context = {'form':form}

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # we don't want to save the user yet
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')  
    return render(request,'login_register.html',context)