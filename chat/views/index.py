from django.shortcuts import redirect, render
from django.urls import reverse
from chat.models.room import Room
from chat.forms import CreateRoom

def index(request):
    rooms = Room.objects.all()
    room = CreateRoom()

    if request.method == 'POST' and 'join_room' in request.POST:
        print(request.POST)
        return redirect(reverse('chat:room', kwargs={'room_name' : request.POST['join_room']}))

    if request.method == 'POST' and 'create_room' in request.POST:
        room = CreateRoom({'name' : request.POST['create_room']})
        if room.is_valid():
            room = room.save()
            return redirect(reverse('chat:room', kwargs={'room_name' : room.id}))

    context = {
        'rooms' : rooms,
        'form' : room
    }
    return render(request, 'index.html', context)