from django.db import models
from django.contrib.auth.models import User

class FriendRequest(models.Model):
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def confirm(self):
        self.confirmed = True
        self.save()
