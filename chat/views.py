from django.shortcuts import render

def index(request):
    return render(request, 'new-index.html')
def room(request, room_name):
    return render(request, 'new-room.html', {
        'room_name': room_name
    })
