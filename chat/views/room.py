from django.shortcuts import render
from chat.models.room import Room
def room(request, room_name):
    room = Room.objects.get(id=room_name)
    return render(request, 'room.html', {
        'room_name': room.name,
        'room_id' : room.id,
    })
