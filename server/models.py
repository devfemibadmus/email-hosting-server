from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class CustomUser(AbstractUser):
    txt_record = models.CharField(max_length=255, default='txt')

    def save(self, *args, **kwargs):
        if not self.txt_record.startswith(f"{settings.MX_RECORD}"):
            self.txt_record = f"{settings.MX_RECORD}{self.username}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_owned_domains(self):
        return Domain.objects.filter(user=self)



class Domain(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    txt_record = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_emails(self):
        return EmailMessage.objects.filter(domain=self)


class SecurityInfo(models.Model):
    tls_enabled = models.BooleanField(default=False)
    tls_version = models.CharField(max_length=20, blank=True, null=True)
    mailed_by = models.CharField(max_length=255, blank=True, null=True)
    signed_by = models.CharField(max_length=255, blank=True, null=True)
    encryption_standard = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"TLS Enabled: {self.tls_enabled}"


class EmailMessage(models.Model):
    sender = models.EmailField()
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
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

    def __str__(self):
        return self.subject
