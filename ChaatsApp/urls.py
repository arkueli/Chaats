from rest_framework import routers
from django.urls import path, include
from django.contrib import admin 
from . import views

router = routers.DefaultRouter()

urlpatterns = [
    path('ChaatsApp/', include(router.urls))
]



















