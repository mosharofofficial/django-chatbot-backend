from django.db import models


class Chat(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=100, default="AI Chat")
    description = models.CharField(max_length=255, default="Ask anything")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=20)  # user / assistant
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
