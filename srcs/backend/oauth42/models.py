from django.contrib.auth.models import User
from django.db import models

from user.models import User42

class UserProfile(models.Model):
    user = models.OneToOneField(User42, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True, null=True)
    id_42 = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)

