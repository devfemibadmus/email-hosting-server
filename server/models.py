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

