from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser, UserProfile, Message
from .serializers import CustomUserSerializer, UserProfileSerializer, MessageSerializer

class CustomUserList(APIView):
    def get(self, request):
        custom_users = CustomUser.objects.all()
        serializer = CustomUserSerializer(custom_users, many=True)
        return Response({'message': 'Custom users retrieved successfully', 'data': serializer.data})

    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Custom user created successfully', 'data': serializer.data})
        return Response({'message': 'Custom user creation failed', 'errors': serializer.errors})

class CustomUserDetail(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            return None

    def get(self, request, pk):
        custom_user = self.get_object(pk)
        if custom_user:
            serializer = CustomUserSerializer(custom_user)
            return Response({'message': 'Custom user retrieved successfully', 'data': serializer.data})
        return Response({'message': 'Custom user not found'}, status=404)

    def put(self, request, pk):
        custom_user = self.get_object(pk)
        if custom_user:
            serializer = CustomUserSerializer(custom_user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Custom user updated successfully', 'data': serializer.data})
            return Response({'message': 'Custom user update failed', 'errors': serializer.errors})
        return Response({'message': 'Custom user not found'}, status=404)

    def delete(self, request, pk):
        custom_user = self.get_object(pk)
        if custom_user:
            custom_user.delete()
            return Response({'message': 'Custom user deleted successfully'})
        return Response({'message': 'Custom user not found'}, status=404)

class UserProfileList(APIView):
    def get(self, request):
        user_profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(user_profiles, many=True)
        return Response({'message': 'User profiles retrieved successfully', 'data': serializer.data})

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User profile created successfully', 'data': serializer.data})
        return Response({'message': 'User profile creation failed', 'errors': serializer.errors})



class MessageList(APIView):
    def get(self, request):
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, many=True)
        return Response({'message': 'Messages retrieved successfully', 'data': serializer.data})

    def post(self, request):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Message created successfully', 'data': serializer.data})
        return Response({'message': 'Message creation failed', 'errors': serializer.errors})



class UserProfileDetail(APIView):
    def get_object(self, pk):
        try:
            return UserProfile.objects.get(pk=pk)
        except UserProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        user_profile = self.get_object(pk)
        if user_profile:
            serializer = UserProfileSerializer(user_profile)
            return Response({'message': 'User profile retrieved successfully', 'data': serializer.data})
        return Response({'message': 'User profile not found'}, status=404)

    def put(self, request, pk):
        user_profile = self.get_object(pk)
        if user_profile:
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'User profile updated successfully', 'data': serializer.data})
            return Response({'message': 'User profile update failed', 'errors': serializer.errors})
        return Response({'message': 'User profile not found'}, status=404)

    def delete(self, request, pk):
        user_profile = self.get_object(pk)
        if user_profile:
            user_profile.delete()
            return Response({'message': 'User profile deleted successfully'})
        return Response({'message': 'User profile not found'}, status=404)

class MessageDetail(APIView):
    def get_object(self, pk):
        try:
            return Message.objects.get(pk=pk)
        except Message.DoesNotExist:
            return None

    def get(self, request, pk):
        message = self.get_object(pk)
        if message:
            serializer = MessageSerializer(message)
            return Response({'message': 'Message retrieved successfully', 'data': serializer.data})
        return Response({'message': 'Message not found'}, status=404)

    def put(self, request, pk):
        message = self.get_object(pk)
        if message:
            serializer = MessageSerializer(message, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Message updated successfully', 'data': serializer.data})
            return Response({'message': 'Message update failed', 'errors': serializer.errors})
        return Response({'message': 'Message not found'}, status=404)

    def delete(self, request, pk):
        message = self.get_object(pk)
        if message:
            message.delete()
            return Response({'message': 'Message deleted successfully'})
        return Response({'message': 'Message not found'}, status=404)

