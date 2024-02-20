from django.shortcuts import render, redirect

def add_friend(request):
    return render(request, 'friend/add_friend.html')
    
def friend_requests(request):
    return render(request, 'friend/friend_requests.html')