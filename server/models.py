from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models

import hashlib

from django.db import models

class VirtualDomain(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class VirtualUser(models.Model):
    domain = models.ForeignKey(VirtualDomain, on_delete=models.CASCADE)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    alt_users = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = hashlib.sha256(self.password.encode()).hexdigest()
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
        return Domain.objects.filter(user=self)

class Domain(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    txt_record = models.CharField(max_length=255)

    def __str__(self):
        return self.name


