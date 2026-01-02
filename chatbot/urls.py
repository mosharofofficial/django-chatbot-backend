from django.contrib import admin
from django.urls import path
from chatbot_app.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # Chat with AI
    path("api/chat/", ChatAPIView.as_view()),

    # AI Chat Rooms: GET all rooms, POST create room
    path("api/ai/rooms/", AiChatRoomsAPIView.as_view()),

    # Messages inside a specific room
    path("api/ai/rooms/<int:room_id>/messages/", RoomMessagesAPIView.as_view()),

    path("api/ai/rooms/<int:room_id>/", delete_ai_room),
    
]
