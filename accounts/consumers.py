from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from channels.db import database_sync_to_async
import json

class AuthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'login':
            await self.handle_login(data)
        elif action == 'register':
            await self.handle_register(data)

    @database_sync_to_async
    def handle_login(self, data):
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            self.send_error('Both username and password are required.')
            return

        user = authenticate(username=username, password=password)
        if user:
            self.send_success('Login successful.')
        else:
            self.send_error('Invalid username or password.')

    @database_sync_to_async
    def handle_register(self, data):
        username = data.get('username')
        password = data.get('password')

        # Validate input
        if not username or not password:
            self.send_error('Both username and password are required.')
            return

        # Check if user with the given username already exists
        if User.objects.filter(username=username).exists():
            self.send_error('Username already exists. Please choose a different one.')
            return

        # Create the user
        user = User.objects.create_user(username=username, password=password)
        if user:
            self.send_success('Registration successful.')
        else:
            self.send_error('Failed to register user.')

    async def send_success(self, message):
        await self.send(text_data=json.dumps({'status': 'success', 'message': message}))

    async def send_error(self, message):
        await self.send(text_data=json.dumps({'status': 'error', 'message': message}))
