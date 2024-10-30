from django.conf import settings
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# from django.utils import timezone


class CustomUser(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',  # Specify a unique related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Specify a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# accounts/models.py


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    verification_token = models.UUIDField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Create a signal to create a Profile when a User is created


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
