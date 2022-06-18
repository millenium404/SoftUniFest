from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    reg_date = models.DateTimeField(auto_now_add=True)
    card_number = models.CharField(max_length=20, blank=True, null=True)
    card_expires = models.CharField(max_length=5, blank=True, null=True)
    notifications = models.BooleanField(default=False)
    is_staff = models.BooleanField(blank=True, null=True)
    is_client = models.BooleanField(blank=True, null=True)
    is_merchant = models.BooleanField(blank=True, null=True)
    password_changed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} Profile'
