from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models



class EmailSettings(models.Model):
    smtp_username = models.CharField(max_length=255, blank=True, null=True)
    smtp_password = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Email Settings for {self.user.email}"
class CustomUser(AbstractUser):
    txt_record = models.CharField(max_length=255, default='txt')
    email_settings = models.OneToOneField("EmailSettings",on_delete=models.CASCADE,null=True,blank=True,related_name="user",)

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


