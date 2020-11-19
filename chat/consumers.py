import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
live_users_count = dict() #Dict to hold current users in each channel
class ChatConsumer(WebsocketConsumer):
    user_status = 'old' #Status to see if user just joined or left or he is old and just sending message
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()
        self.user_status = 'new' #User just joined
        try: #See if we have this channel in users_count
            live_users_count[self.room_name]
        except:
            live_users_count[self.room_name] = 0
        self.receive(json.dumps({'message':'|--User joined the channel--|'})) #Send message to channel that user joined
    def disconnect(self, close_code):
        # Leave room group
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        self.user_status = 'left' #User left
        self.receive(json.dumps({'message':'|--User left the channel--|'})) #Send message that user left the channel
    # Receive message from WebSocket
    def count_users(self): #To send add or remove users from online users field
        #self.live_users = 0
        all_dict = dict()
        try:
            all_dict[self.room_name]
        except:
            all_dict[self.room_name] = 0
            all_dict[self.room_name]
        if self.user_status == 'new':
            all_dict[self.room_name] = 1
            self.user_status = 'old'
        elif self.user_status == 'left':
            all_dict[self.room_name] = -1
            self.user_status = 'old'
        else:
            all_dict[self.room_name] = 0
        return all_dict[self.room_name]
    def receive(self, text_data):
        global live_users_count
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Live users count

        live_users_count[self.room_name] += self.count_users()
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'live' : live_users_count[self.room_name],
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']
        live = event['live']
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'live' : live
        }))
    

