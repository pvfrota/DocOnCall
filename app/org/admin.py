
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import OrgUnit, OrgUnitMembership, OrgUnitType


@admin.register(OrgUnit)
class OrgUnitAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "parent_link", "is_schedulable")
    list_filter = ("type", "is_schedulable")
    search_fields = ("name",)
    ordering = ("name",)

    @admin.display(description="Parent", ordering="parent__name")
    def parent_link(self, obj: OrgUnit):
        if not obj.parent:
            return "–"
        url = reverse("admin:org_orgunit_change", args=[obj.parent_id])
        return format_html('<a href="{}">{}</a>', url, obj.parent.name)

@admin.register(OrgUnitMembership)
class OrgUnitMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "org_unit", "role", "can_take_shifts", "priority")
    list_filter = ("role", "can_take_shifts")
    search_fields = ("user__username", "org_unit__name")
