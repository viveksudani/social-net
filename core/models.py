from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True)
    friends = models.ManyToManyField("self", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return self.email


class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ("Accepted", "Accepted"),
        ("Rejected", "Rejected"),
        ("Pending", "Pending"),
    )
    sender = models.ForeignKey(User, models.CASCADE, related_name="sent_requests")
    receiver = models.ForeignKey(User, models.CASCADE, related_name="received_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default="Pending")
