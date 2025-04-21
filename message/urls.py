from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat, name='chat'),  # This will now match /messages/
    path('<str:username>/', views.get_messages, name='get_messages'),
    path('send/', views.send_message, name='send_message'),
    path('contacts/', views.chat_contacts, name='chat_contacts'),
]