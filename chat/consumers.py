import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from chat.models.room import Room


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

        room = Room.objects.filter(name=self.room_name).last()
        room.current_users += 1 if room.current_users >= 0 else 0
        room.save()

        #Send message to channel that user joined
        self.receive(json.dumps({'message':'|--User joined the channel--|', 'live' : room.current_users}))

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        
        room = Room.objects.filter(name=self.room_name).last()
        if room.current_users > 1:
            room.current_users -= 1
            room.save()
            live = room.current_users
        else:
            room.delete()
            live = 0

        #Send message to channel that user joined
        self.receive(json.dumps({'message':'|--User left the channel--|', 'live' : live}))

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        live = text_data_json['live'] if 'live' in text_data_json else None

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'live' : live,
            }
        )

    # Receive message from room group
    def chat_message(self, event):

        message = event['message']
        live = event['live']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'live': live,
        }))
    

