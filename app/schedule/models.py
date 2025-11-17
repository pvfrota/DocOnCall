from django.db import models

from doconcall import settings


class AvailabilitySlot(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_slots",
    )
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    label = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'schedule_availability_slot'
        ordering = ["start_at"]

    def __str__(self):
        return f"{self.user} disponível de {self.start_at} a {self.end_at}"


class Event(models.Model):
    class Kind(models.TextChoices):
        INTERNAL_SHIFT = "INTERNAL_SHIFT", "Plantão interno"
        EXTERNAL_SHIFT = "EXTERNAL_SHIFT", "Plantão externo"
        PERSONAL = "PERSONAL", "Pessoal"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="events",
    )

    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    kind = models.CharField(max_length=20, choices=Kind.choices)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ["start_at"]

    def __str__(self):
        return f"{self.title} ({self.start_at} - {self.end_at})"
