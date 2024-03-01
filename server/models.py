from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class VirtualDomains(models.Model):
    name = models.CharField(max_length=255)
    txt_record = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message_tag = models.CharField(max_length=100, blank=True)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_virtual_users(self):
        return VirtualUsers.objects.filter(domain=self)

class VirtualAliases(models.Model):
    domain_id = models.IntegerField()
    source = models.EmailField()
    destination = models.EmailField()

    def __str__(self):
        return self.domain_id

class VirtualUsers(models.Model):
    domain_id = models.IntegerField()
    password = models.CharField(max_length=255)
    email = models.EmailField()
    alt_users = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.password:
            self.password = hashlib.sha512(self.password.encode()).hexdigest()
        super().save(*args, **kwargs)

class CustomUser(AbstractUser):
    txt_record = models.CharField(max_length=255, default='txt')

    def save(self, *args, **kwargs):
        if not self.txt_record.startswith(f"{settings.MX_RECORD}"):
            self.txt_record = f"{settings.MX_RECORD}{self.username}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_owned_domains(self):
        return VirtualDomains.objects.filter(user=self)
