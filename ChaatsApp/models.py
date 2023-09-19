from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    groups = models.ManyToManyField(
            'auth.Group',
            verbose_name='groups',
            blank=True,
            help_text='The groups this user belongs to.',
            related_name='customuser_set', 
        )
    user_permissions = models.ManyToManyField(
            'auth.Permission',
            verbose_name='user permissions',
            blank=True,
            help_text='Specific permissions for this user.',
            related_name='customuser_set',  
        )

    def __str__(self):
        return self.username

   

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return self.user.username




class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username} to {self.receiver.username}'

    class Meta:
        ordering = ('timestamp',)


