import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import TokenError, RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenVerifySerializer
from django.contrib.auth import authenticate, login
from channels.db import database_sync_to_async 
from django.db import models
from models import Message, UserProfile, CustomUser
from serializers import CustomUserSerializer, UserProfileSerializer, MessageSerializer


User = get_user_model()

class UserAuthConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Authenticate the WebSocket connection using JWT token
        authentication_status = await self.authenticate_websocket()
        if authentication_status == "authenticated":
            await self.accept()
        elif authentication_status == "authentication_failed":
            await self.close(code=1008)  # Close WebSocket connection with status 1008 

    async def authenticate_websocket(self):
        try:
            token_data = await self.get_token_data()
            if token_data and 'user_id' in token_data:
                user = User.objects.get(id=token_data['user_id'])
                if user.is_authenticated:
                    return "authenticated"
        except TokenError:
            pass

        # Authentication failed
        return "authentication_failed"

    async def get_token_data(self):
        try:
            token = self.scope["user"]
            serializer = TokenVerifySerializer(data={'token': token})
            serializer.is_valid(raise_exception=True)
            return serializer.validated_data
        except TokenError:
            return None


   

class ChatMessage(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'direct_message':
            await self.send_direct_message(data)
        elif action == 'receive_message':
            await self.receive_message(data)
        elif action == 'message_history':
            await self.get_message_history(data)
      

    async def send_direct_message(self, data):
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        content = data.get('content')

        # Create new message
        message = Message.objects.create(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content
        )

        message.save()

        # Send the message via WebSocket to receiver
        await self.send(text_data=json.dumps({
            'action': 'direct_message',
            'message_id': message.id,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        }))

        # Notify sender
        await self.send(text_data=json.dumps({
            'action': 'message_sent',
            'message_id': message.id,
        }))


    async def get_message_history(self, data):
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')

        # Retrieve message history between sender and receiver
        messages = Message.objects.filter(            
            (models.Q(sender_id=sender_id, receiver_id=receiver_id) |
             models.Q(sender_id=receiver_id, receiver_id=sender_id))
        ).order_by('timestamp')

        message_history = []

        for message in messages:
            message_history.append({
                'message_id': message.id,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            })

        await self.send(text_data=json.dumps({
            'action': 'message_history',
            'message_history': message_history,
        }))

class UserProfileConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'list_users':
            await self.list_all_users()
        elif action == 'get_profile':
            user_id = data.get('user_id')
            await self.retrieve_user_profile(user_id)
        elif action == 'update_profile':
            await self.update_user_profile(data)

    @database_sync_to_async
    def list_all_users(self):
        users = UserProfile.objects.all()
        user_list = UserProfileSerializer(users, many=True).data

        # Send the list of users to the WebSocket client
        self.send_json({'action': 'list_users', 'users': user_list})

    @database_sync_to_async
    def retrieve_user_profile(self, user_id):
        # Query and retrieve the user profile data based on the provided user_id
        try:
            user_profile = UserProfile.objects.get(id=user_id)
            user_data = UserProfileSerializer(user_profile).data

            # Send the user profile data to the WebSocket client
            self.send_json({'action': 'get_profile', 'user': user_data})
        except UserProfile.DoesNotExist:
            # Handle the case where the user profile doesn't exist
            self.send_json({'action': 'get_profile', 'error': 'User not found'})

    @database_sync_to_async
    def update_user_profile(self, data):
        # Extract, update, and save user profile data
        user_id = data.get('user_id')
        new_data = {
            'email': data.get('email'),
            'first_name': data.get('first_name'),
            'last_name': data.get('last_name'),
            'profile_picture': data.get('profile_picture')
        }

        try:
            user_profile = UserProfile.objects.get(id=user_id)

            for key, value in new_data.items():
                setattr(user_profile, key, value)

            user_profile.save()

            # Send a success message to the WebSocket client
            self.send_json({'action': 'update_profile', 'message': 'Profile updated successfully'})
        except UserProfile.DoesNotExist:
            # Handle the case where the user profile doesn't exist
            self.send_json({'action': 'update_profile', 'error': 'User not found'})



class ChatConsumer(AsyncWebsocketConsumer):
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'typing':
            await self.handle_typing(data)
        elif action == 'user_status':
            await self.handle_user_status(data)

    async def handle_typing(self, data):
        # Handle typing event
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        is_typing = data.get('is_typing')

        # Notify the receiver about typing status
        await self.send_user_typing_status(receiver_id, sender_id, is_typing)

    async def handle_user_status(self, data):
        # Handle user status change event
        user_id = data.get('user_id')
        status = data.get('status')


    async def send_user_typing_status(self, receiver_id, sender_id, is_typing):
        # Notify the receiver of typing status of sender
        await self.send(text_data=json.dumps({
            'action': 'typing',
            'sender_id': sender_id,
            'receiver_id': receiver_id,
            'is_typing': is_typing,
        }))











