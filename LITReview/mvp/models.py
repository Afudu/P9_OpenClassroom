from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

class User(AbstractUser):
    """Custom User model inheriting from AbstractUser."""
    DoesNotExist = None
    pass


class UserFollows(models.Model):
    """Model to represent follow relationships between users."""
    DoesNotExist = None
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    followed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')

    class Meta:
        """Meta class to ensure unique follow relationships."""
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f'{self.user} follows {self.followed_user}'


class Ticket(models.Model):
    objects = None
    title = models.CharField(max_length=128, blank=False, default='')
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    image = models.ImageField(null=True, blank=True, upload_to="ticket_images")
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    objects = None
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 1 and 5
        validators=[MinValueValidator(1), MaxValueValidator(5)])
    headline = models.CharField(max_length=128)
    body = models.CharField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(default=timezone.now)
