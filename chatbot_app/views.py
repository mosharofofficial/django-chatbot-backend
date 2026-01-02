from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from litellm import completion
from .models import Chat, Message
from .serializers import *
from rest_framework.decorators import api_view

class ChatAPIView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        messages_data = request.data.get("messages", [])
        if not messages_data:
            return Response({"error": "Messages required"}, status=status.HTTP_400_BAD_REQUEST)

 
        chat_id = request.data.get("chat_id")
        if chat_id:
            chat = Chat.objects.filter(id=chat_id, email=email).first()
            if not chat:
                return Response({"error": "Chat not found"}, status=404)
        else:
            chat = Chat.objects.create(email=email)
 

        for msg in messages_data:
            if msg["role"] == "user":
                Message.objects.create(
                    chat=chat, role="user", content=msg["content"])

  
        all_msgs = []
        for msg in chat.messages.all().order_by("created_at"):
            all_msgs.append({"role": msg.role, "content": msg.content})

 
        response = completion(
            model="groq/qwen/qwen3-32b",
            messages=all_msgs
        )

        reply = response.choices[0].message.content
        if reply.startswith("<think>"):
            reply = reply.split("</think>")[-1].strip()

 
        Message.objects.create(chat=chat, role="assistant", content=reply)

        return Response({
            "chat_id": chat.id,
            "reply": reply
        })


class AiChatRoomsAPIView(APIView):
    """
    GET: List all AI chat rooms
    POST: Create a new AI chat room
    """
    def get(self, request):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        rooms = Chat.objects.filter(email=email)
        serializer = ChatRoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request):
        email = request.data.get("email")
        name = request.data.get("name", "AI Chat")
        description = request.data.get("description", "Ask anything")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        # Create new room
        room = Chat.objects.create(email=email, name=name, description=description)
        serializer = ChatRoomSerializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RoomMessagesAPIView(APIView):
    """
    GET /api/ai/rooms/<int:room_id>/messages?email=user@example.com
    """

    def get(self, request, room_id):
        email = request.query_params.get("email")
        if not email:
            return Response({"error": "email is required"}, status=400)

        chat = Chat.objects.filter(id=room_id, email=email).first()
        if not chat:
            return Response({"error": "Room not found"}, status=404)

        messages = chat.messages.all().order_by("created_at")
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)


class CreateRoomAPIView(APIView):
    """
    POST /api/ai/rooms
    Body: {
        "email": "user@example.com",
        "name": "New Room",
        "description": "Optional description"
    }
    """

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "email is required"}, status=400)

        name = request.data.get("name", "AI Chat")
        description = request.data.get("description", "Ask anything")

        chat = Chat.objects.create(
            email=email,
            name=name,
            description=description
        )

        serializer = ChatRoomSerializer(chat)
        return Response(serializer.data, status=201)


@api_view(['DELETE'])
def delete_ai_room(request, room_id):
    

    room = Chat.objects.filter(id=room_id).first()
    if not room:
        return Response({"error": "Room not found"}, status=404)

    room.delete()
    return Response({"success": True}, status=200)
