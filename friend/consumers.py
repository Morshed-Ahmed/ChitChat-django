# import json
# from channels.generic.websocket import WebsocketConsumer
# from .models import FriendRequest

# class FriendRequestConsumer(WebsocketConsumer):
#     def connect(self):
#         self.accept()

#     def disconnect(self, close_code):
#         pass

#     def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get('action')

#         if action == 'search_users':
#             data = json.loads(text_data)
#             query = data.get('query')
#             if query:
#                 users = User.objects.filter(username__icontains=query)
#                 users_list = [{'id': user.id, 'username': user.username} for user in users]
#                 self.send(text_data=json.dumps({'users': users_list}))
#         elif action == 'add_friend_request':
#             sender_id = data.get('sender_id')
#             receiver_id = data.get('receiver_id')
#             # Create a friend request instance
#             friend_request = FriendRequest.objects.create(sender_id=sender_id, receiver_id=receiver_id)
#             # Add sender to the group of the receiver
#             self.channel_layer.group_add(
#                 f"user_{receiver_id}",
#                 self.channel_name
#             )
#             # You may also send a notification to the receiver via channels or any other means
#             notification_data = {
#                 'notification': 'You have received a friend request!'
#             }
#             # Send the notification to the receiver's WebSocket channel
#             self.send(text_data=json.dumps(notification_data))

#     # def friend_request_notification(self, event):
#     #     # Send notification to the group
#     #     self.send(text_data=json.dumps({
#     #         'notification': event['notification']
#     #     }))


import json
from channels.generic.websocket import WebsocketConsumer
from .models import FriendRequest
from django.contrib.auth.models import User

class UserSearchConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        query = data.get('query')
        if query:
            users = User.objects.filter(username__icontains=query)
            users_list = [{'id': user.id, 'username': user.username} for user in users]
            self.send(text_data=json.dumps({'users': users_list}))

class FriendRequestConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')
        if action == 'send_friend_request':
            sender_id = data.get('sender_id')
            receiver_id = data.get('receiver_id')
            friend_request = FriendRequest.objects.create(sender_id=sender_id, receiver_id=receiver_id)
            # Send confirmation to sender
            self.send(text_data=json.dumps({'message': 'Friend request sent'}))
            # Send notification to receiver
            receiver_channel_name = f"user_{receiver_id}"
            self.channel_layer.send(receiver_channel_name, {'type': 'friend_request_notification'})

    def friend_request_notification(self, event):
        self.send(text_data=json.dumps({'notification': 'You have received a friend request'}))
