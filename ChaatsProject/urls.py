from django.urls import path
from ChaatsApp.views import (
    CustomUserList,
    CustomUserDetail,
    UserProfileList,
    UserProfileDetail,
    MessageList,
    MessageDetail,
)

urlpatterns = [
    path('custom-users/', CustomUserList.as_view(), name='customuser-list'),
    path('custom-users/<int:pk>/', CustomUserDetail.as_view(), name='customuser-detail'),
    path('user-profiles/', UserProfileList.as_view(), name='userprofile-list'),
    path('user-profiles/<int:pk>/', UserProfileDetail.as_view(), name='userprofile-detail'),
    path('messages/', MessageList.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageDetail.as_view(), name='message-detail'),
    
]
