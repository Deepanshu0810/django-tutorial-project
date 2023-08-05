from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerPage,name='register'),
    path('user/<str:pk>/',views.userProfile,name='user'),

    # mobile views
    path('activity/',views.activity,name='activity'),
    path('topics/',views.topics,name='topics'),

    path('room/<str:pk>/',views.room,name='room'),
    path('delete-message/<str:pk>/',views.deleteMessage,name='delete-message'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>/',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>/',views.deleteRoom,name='delete-room'),
    path('update-user/',views.updateUser,name='update-user'),
]