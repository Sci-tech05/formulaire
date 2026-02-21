from django.db import models
from django.core.validators import RegexValidator
import shortuuid


def generate_ticket_number():
    """Génère un numéro de ticket séquentiel de type EE-2026-001."""
    last = Participant.objects.order_by('-id').first()
    if last and last.ticket_number:
        try:
            seq = int(last.ticket_number.split('-')[-1]) + 1
        except (ValueError, IndexError):
            seq = Participant.objects.count() + 1
    else:
        seq = 1
    return f"EE-2026-{seq:03d}"


class Participant(models.Model):
    whatsapp_validator = RegexValidator(
        regex=r'^\+?[0-9]{8,15}$',
        message=(
            "Numéro invalide. Utilisez le format international, ex : "
            "+22967000000 ou +33612345678"
        ),
    )

    nom = models.CharField("Nom", max_length=100)
    prenom = models.CharField("Prénom", max_length=100)
    whatsapp = models.CharField(
        "Numéro WhatsApp",
        max_length=20,
        unique=True,
        validators=[whatsapp_validator],
        help_text="Format : +22967xxxxxx ou numéro international",
    )
    etablissement = models.CharField(
        "Établissement / Filière",
        max_length=200,
        blank=True,
        default="",
        help_text="Ex : ENSET – Génie Électrique",
    )
    ticket_number = models.CharField(
        "Numéro de ticket",
        max_length=20,
        unique=True,
        blank=True,
    )
    created_at = models.DateTimeField("Date d'inscription", auto_now_add=True)

    class Meta:
        verbose_name = "Participant"
        verbose_name_plural = "Participants"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.prenom} {self.nom} — {self.ticket_number}"

    @property
    def nom_complet(self):
        return f"{self.prenom} {self.nom}"

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            self.ticket_number = generate_ticket_number()
        super().save(*args, **kwargs)
