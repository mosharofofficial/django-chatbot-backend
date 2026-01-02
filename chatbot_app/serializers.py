from rest_framework import serializers
from .models import Chat, Message


class LastMessageSerializer(serializers.Serializer):
    text = serializers.CharField()
    createdAt = serializers.DateTimeField()


class ChatRoomSerializer(serializers.ModelSerializer):
    lastMessage = serializers.SerializerMethodField()
    updatedAt = serializers.DateTimeField(source="updated_at")

    class Meta:
        model = Chat
        fields = ["id", "name", "description", "lastMessage", "updatedAt"]

    def get_lastMessage(self, chat):
        last_msg = chat.messages.order_by("-created_at").first()
        if not last_msg:
            return None

        return {
            "text": last_msg.content,
            "createdAt": last_msg.created_at
        }


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["role", "content", "created_at"]
