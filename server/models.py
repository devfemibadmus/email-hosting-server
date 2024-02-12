from django.contrib.auth.models import AbstractUser
from django.db import models

class Subscription(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class CustomUser(AbstractUser):
    subscriptions = models.ManyToManyField(Subscription, related_name='subscribers', blank=True)

class SecurityInfo(models.Model):
    tls_enabled = models.BooleanField(default=False)
    tls_version = models.CharField(max_length=20, blank=True, null=True)
    mailed_by = models.CharField(max_length=255, blank=True, null=True)
    signed_by = models.CharField(max_length=255, blank=True, null=True)
    encryption_standard = models.CharField(max_length=255, blank=True, null=True)

class EmailMessage(models.Model):
    sender = models.EmailField()
    recipients = models.ManyToManyField(CustomUser, related_name='received_messages')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)
    category_choices = (
        ('inbox', 'Inbox'),
        ('sent', 'Sent'),
        ('spam', 'Spam'),
    )
    category = models.CharField(max_length=10, choices=category_choices)
    security_info = models.OneToOneField(SecurityInfo, on_delete=models.CASCADE, related_name='email_message', null=True, blank=True)

class Domain(models.Model):
    name = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_created=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='domains')
