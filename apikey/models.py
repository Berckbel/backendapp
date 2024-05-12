from django.db import models
from django.contrib.auth.models import User
import secrets

class APIKey(models.Model):
    key = models.CharField(max_length=100, default=secrets.token_urlsafe(32))
    user = models.ForeignKey(User, related_name="user_apikey", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " key: " + self.key
