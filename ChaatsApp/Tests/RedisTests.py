from channels.layers import get_channel_layer
from channels.testing import ChannelsLiveServerTestCase
import json
from channels.db import database_sync_to_async
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from ChaatsApp.consumers import ChatConsumer  


class UserAuthConsumerTests(ChannelsLiveServerTestCase):

    async def test_user_auth_redis_interaction(self):
        # Connect to the WebSocket
        communicator = await self.connect()

        # Publish a message to a Redis channel, simulating authentication
        channel_layer = get_channel_layer()
        await channel_layer.group_add("auth", communicator.channel_name)
        await channel_layer.group_send("auth", {
            "type": "auth.message",
            "message": "User authenticated"
        })

        # Receive the Redis-published message via WebSocket
        response = await communicator.receive_json_from()

        # Check if the message from Redis is as expected
        self.assertEqual(response["message"], "User authenticated")

        # Disconnect from the WebSocket
        await communicator.disconnect()


class ChatMessageConsumerTests(ChannelsLiveServerTestCase):
    async def test_chat_message_redis_interaction(self):
        # Connect to the WebSocket
        communicator = await self.connect()

        # Create a test message
        test_message = {
            "action": "direct_message",
            "sender_id": 1,
            "receiver_id": 2,
            "content": "Hello, world!"
        }

        # Publish the test message to a Redis channel
        channel_layer = get_channel_layer()
        await channel_layer.group_add("chat", communicator.channel_name)
        await channel_layer.group_send("chat", {
            "type": "chat.message",
            "message": json.dumps(test_message)
        })

        # Receive the Redis-published message via WebSocket
        response = await communicator.receive_json_from()

        # Check if the received message matches the test message
        self.assertEqual(response, test_message)

        # Disconnect from the WebSocket
        await communicator.disconnect()


class ChatConsumerTests(TestCase):
    async def test_chat_consumer(self):
        # Create a WebSocket communicator for testing
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")

        # Connect to the WebSocket
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        try:
            # Simulate receiving a message
            await communicator.send_json_to({
                "action": "typing",
                "sender_id": 1,
                "receiver_id": 2,
                "is_typing": True,
            })

            # Expect to receive a message in response
            response = await communicator.receive_json_from()
            self.assertEqual(response["action"], "typing")
            self.assertEqual(response["sender_id"], 1)
            self.assertEqual(response["receiver_id"], 2)
            self.assertEqual(response["is_typing"], True)

            # Simulate another action
            await communicator.send_json_to({
                "action": "user_status",
                "user_id": 1,
                "status": "online",
            })

            # Expect to receive a message for the user status
            response = await communicator.receive_json_from()
            self.assertEqual(response["action"], "user_status")
            self.assertEqual(response["user_id"], 1)
            self.assertEqual(response["status"], "online")

        finally:
            # Close the WebSocket
            await communicator.disconnect()



