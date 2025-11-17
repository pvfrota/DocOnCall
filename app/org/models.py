
from django.db import models
from django.conf import settings


class OrgUnitType(models.TextChoices):
    ORGANIZATION = "ORGANIZATION", "Organização / Grupo"
    FACILITY = "FACILITY", "Unidade física (hospital, clínica)"
    DEPARTMENT = "DEPARTMENT", "Setor / Serviço"
    UNIT = "UNIT", "Unidade / Ala"
    SUBSCALE = "SUBSCALE", "Sub-escala"
    TEAM = "TEAM", "Time"
    CUSTOM = "CUSTOM", "Customizado"


class OrgUnit(models.Model):
    name = models.CharField(max_length=200)
    type = models.CharField(
        max_length=20,
        choices=OrgUnitType.choices,
        default=OrgUnitType.ORGANIZATION,
    )

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="children",
    )

    is_schedulable = models.BooleanField(
        default=False,
        help_text="Se pode ter plantões/turnos diretamente associados a este nó.",
    )

    conflict_scope_parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="conflict_children",
        help_text="Nó pai para conflito agregado (ex.: Semi + Enfermaria → Clínica Médica)",
    )

    metadata = models.JSONField(null=True, blank=True)

    @property
    def full_name(self):
        parts = [self.name]
        parent = self.parent
        while parent:
            parts.append(parent.name)
            parent = parent.parent
        return " - ".join(reversed(parts))

    class Meta:
        db_table = 'org_unit'
        verbose_name = "Organizational Unit"
        verbose_name_plural = "Organizational Units"

    def __str__(self):
        return self.full_name


class OrgUnitMembership(models.Model):
    class Role(models.TextChoices):
        MEMBER = "MEMBER", "Membro"
        MANAGER = "MANAGER", "Gerente"
        ADMIN = "ADMIN", "Administrador da unidade"
        VIEWER = "VIEWER", "Somente visualização"

    org_unit = models.ForeignKey(
        OrgUnit, on_delete=models.CASCADE, related_name="memberships"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="org_memberships"
    )

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.MEMBER)

    can_take_shifts = models.BooleanField(
        default=True,
        help_text="Se este usuário pode assumir plantões nesta unidade.",
    )

    # útil para escalonamento:
    priority = models.PositiveIntegerField(
        default=100,
        help_text="Ordem opcional de prioridade base para este usuário na unidade.",
    )

    class Meta:
        db_table = 'org_unit_membership'
        unique_together = ("org_unit", "user")
        ordering = ["priority"]

    def __str__(self):
        return f"{self.user} @ {self.org_unit} ({self.role})"
