from django.contrib import admin
from .models import AvailabilitySlot, Event


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("user", "start_at", "end_at", "label")
    list_filter = ("user",)
    ordering = ("start_at",)


@admin.register(Event)
class ScheduleEventAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "kind", "start_at", "end_at")
    list_filter = ("user", "kind")
    ordering = ("start_at",)
