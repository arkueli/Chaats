from channels.testing import ChannelsLiveServerTestCase, ApplicationCommunicator
from django.urls import reverse
from django.contrib.auth import get_user_model
from ChaatsApp.models import Message, UserProfile, UserProfile  
from ChaatsApp.routing import websocket_urlpatterns  
from django.urls import re_path
from . import consumers
from ChaatsApp.serializers import UserProfileSerializer  
from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase
import json

class UserAuthConsumerTests(ChannelsLiveServerTestCase):

    async def test_user_auth_consumer(self):
        # Connect to the WebSocket
        communicator = await self.connect()

        # Send a WebSocket message to authenticate
        await communicator.send_json_to({
            "type": "authenticate.websocket",
            "token": "your_jwt_token_here"
        })

        # Receive a WebSocket message
        response = await communicator.receive_json_from()

        # Check if the authentication response is as expected
        self.assertEqual(response["authentication_status"], "authenticated")

        # Disconnect from the WebSocket
        await communicator.disconnect()


User = get_user_model()

class ChatMessageConsumerTestCase(ChannelsLiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password'
        )

    def test_chat_message_consumer(self):
        communicator = ApplicationCommunicator(websocket_urlpatterns, {
            "type": "websocket.connect",
            "path": reverse("r'ws/chat-message/$', consumers.ChatMessage.as_asgi()"),  
        })

        connected, _ = communicator.connect()
        self.assertTrue(connected)

        # Simulate authentication by sending a JWT token
        communicator.send_json_to({
            "type": "authenticate",
            "token": "YOUR_JWT_TOKEN_HERE", 
        })

        response = communicator.receive_json_from()
        self.assertEqual(response, {"type": "authenticated"})

        # Simulate sending a direct message
        communicator.send_json_to({
            "type": "send_direct_message",
            "sender_id": self.user.id,
            "receiver_id": 2,  # Replace with a valid receiver ID
            "content": "Hello, World!",
        })

        response = communicator.receive_json_from()
        self.assertEqual(response["type"], "direct_message")
        self.assertIn("message_id", response)
        self.assertEqual(response["content"], "Hello, World!")

        # Disconnect the communicator
        communicator.disconnect()
        self.assertIsNone(communicator.receive_nothing())
        

class UserProfileConsumerTestCase(ChannelsLiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='test_password'
        )

    def test_user_profile_consumer(self):
        communicator = ApplicationCommunicator(websocket_urlpatterns, {
            "type": "websocket.connect",
            "path": reverse("r'ws/user-profile/$', consumers.UserProfileConsumer.as_asgi()"), 
        })

        connected, _ = communicator.connect()
        self.assertTrue(connected)

        # Simulate authentication by sending a JWT token
        communicator.send_json_to({
            "type": "authenticate",
            "token": "JWT_TOKEN_HERE",
        })

        response = communicator.receive_json_from()
        self.assertEqual(response, {"type": "authenticated"})

        # Simulate listing all users
        communicator.send_json_to({
            "type": "list_users",
        })

        response = communicator.receive_json_from()
        self.assertEqual(response["type"], "list_users")
        self.assertIn("users", response)

        # Simulate retrieving a user profile
        communicator.send_json_to({
            "type": "get_profile",
            "user_id": self.user.id,  # Replace with a valid user ID
        })

        response = communicator.receive_json_from()
        self.assertEqual(response["type"], "get_profile")
        self.assertIn("user", response)

        # Simulate updating a user profile
        communicator.send_json_to({
            "type": "update_profile",
            "user_id": self.user.id,  # Replace with a valid user ID
            "email": "new_email@example.com",
            "first_name": "New First Name",
            "last_name": "New Last Name",
            "profile_picture": "new_picture.jpg",
        })

        response = communicator.receive_json_from()
        self.assertEqual(response["type"], "update_profile")
        self.assertIn("message", response)

        # Disconnect the communicator
        communicator.disconnect()
        self.assertIsNone(communicator.receive_nothing())


class ChatConsumerTestCase(ChannelsLiveServerTestCase):
    def setUp(self):
        self.sender_profile = UserProfile.objects.create(username='sender')
        self.receiver_profile = UserProfile.objects.create(username='receiver')

    def test_chat_consumer(self):
        communicator_sender = ApplicationCommunicator(websocket_urlpatterns, {
            "type": "websocket.connect",
            "path": reverse("r'ws/chat/$', consumers.ChatConsumer.as_asgi()"), 
        })

        communicator_receiver = ApplicationCommunicator(websocket_urlpatterns, {
            "type": "websocket.connect",
            "path": reverse("r'ws/chat/$', consumers.ChatConsumer.as_asgi()"),  
        })

        connected_sender, _ = communicator_sender.connect()
        connected_receiver, _ = communicator_receiver.connect()
        self.assertTrue(connected_sender)
        self.assertTrue(connected_receiver)

        # Simulate sending typing status
        communicator_sender.send_json_to({
            "type": "typing",
            "sender_id": self.sender_profile.id,
            "receiver_id": self.receiver_profile.id,
            "is_typing": True,
        })

        response = communicator_receiver.receive_json_from()
        self.assertEqual(response["type"], "typing")
        self.assertEqual(response["sender_id"], str(self.sender_profile.id))
        self.assertEqual(response["receiver_id"], str(self.receiver_profile.id))
        self.assertEqual(response["is_typing"], True)

        # Simulate sending user status change
        communicator_sender.send_json_to({
            "type": "user_status",
            "user_id": self.sender_profile.id,
            "status": "away",
        })

        response = communicator_receiver.receive_json_from()
        self.assertEqual(response["type"], "user_status")
        self.assertEqual(response["user_id"], str(self.sender_profile.id))
        self.assertEqual(response["status"], "away")

        # Disconnect communicators
        communicator_sender.disconnect()
        communicator_receiver.disconnect()
        self.assertIsNone(communicator_sender.receive_nothing())
        self.assertIsNone(communicator_receiver.receive_nothing())



