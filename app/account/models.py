from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    DOCTOR = "DOCTOR", "Médico"
    HOSPITAL_ADMIN = "HOSPITAL_ADMIN", "Admin do hospital"
    INTERNAL_STAFF = "INTERNAL_STAFF", "Equipe interna"


class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.DOCTOR,
    )

    def __str__(self):
        return f'({self.id}) {self.get_full_name() or self.username}'


class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor",
    )
    crm = models.CharField(max_length=50, blank=True, null=True)
    specialty = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user
