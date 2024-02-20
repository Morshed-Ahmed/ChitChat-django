# urls.py

from django.urls import path
from . import views

urlpatterns = [
   
    path('add-friend/', views.add_friend, name='add_friend'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
   
]
