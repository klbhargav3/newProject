from django.db import models
from django.contrib.auth.models import User

class Conversation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="conversations")
    title=models.CharField(max_length=200,default="New Chat")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

class Messages(models.Model):
    conversation=models.ForeignKey(Conversation,on_delete=models.CASCADE,related_name="messages")
    sender=models.CharField(max_length=30,choices=(("user","User"),("assistant","Assistant")))
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender
