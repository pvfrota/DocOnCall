from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Role", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_superuser")
    list_filter = ("role", "is_staff", "is_superuser")


@admin.register(Doctor)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "crm", "specialty")
    search_fields = ("user__username", "user__first_name", "user__last_name", "crm")
