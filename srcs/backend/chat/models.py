from django.db import models
from user.models import User42 

class PrivateMessage(models.Model):
    sender = models.ForeignKey(User42, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User42, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username} - {self.message[:20]}"

class BlockedUser(models.Model):
    blocker = models.ForeignKey(User42, related_name='blocker', on_delete=models.CASCADE)
    blocked = models.ForeignKey(User42, related_name='blocked', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('blocker', 'blocked')

    def __str__(self):
        return f"{self.blocker.username} a bloque {self.blocked.username}"
    
