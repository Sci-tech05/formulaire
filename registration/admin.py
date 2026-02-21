from django.contrib import admin
from django.utils.html import format_html
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from import_export import resources
from import_export.admin import ExportMixin
from import_export.formats.base_formats import XLSX, CSV, Format
import io

from .models import Participant


# ─── Format PDF personnalisé ───────────────────────────────────────────────
class PDFFormat(Format):
    """Format PDF utilisant WeasyPrint + template admin_export_pdf.html."""

    def get_title(self):
        return 'PDF'

    def get_extension(self):
        return 'pdf'

    def get_content_type(self):
        return 'application/pdf'

    def is_binary(self):
        return True

    def can_export(self):
        return True

    def can_import(self):
        return False

    def export_data(self, resource, queryset=None, **kwargs):
        # Appelé par ExportMixin — on génère le PDF ici
        from django.conf import settings
        participants = (queryset or resource.get_queryset()).order_by('created_at')
        total = participants.count()
        max_places = getattr(settings, 'EVENT_MAX_PLACES', 100)

        html_string = render_to_string('admin_export_pdf.html', {
            'participants': participants,
            'total': total,
            'places_restantes': max(0, max_places - Participant.objects.count()),
            'max_places': max_places,
            'generated_at': timezone.now(),
        })
        from weasyprint import HTML
        pdf_file = io.BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)
        return pdf_file.getvalue()


# ─── Resource ─────────────────────────────────────────────────────────────
class ParticipantResource(resources.ModelResource):
    class Meta:
        model = Participant
        fields = ('ticket_number', 'nom', 'prenom', 'whatsapp', 'etablissement', 'created_at')
        export_order = ('ticket_number', 'nom', 'prenom', 'whatsapp', 'etablissement', 'created_at')


# ─── Action PDF (sélection manuelle) ─────────────────────────────────────
def export_participants_pdf(modeladmin, request, queryset):
    """Action admin : exporte la sélection en PDF via WeasyPrint."""
    from django.conf import settings
    participants = queryset.order_by('created_at')
    total = participants.count()
    max_places = getattr(settings, 'EVENT_MAX_PLACES', 100)
    html_string = render_to_string('admin_export_pdf.html', {
        'participants': participants,
        'total': total,
        'places_restantes': max(0, max_places - Participant.objects.count()),
        'max_places': max_places,
        'generated_at': timezone.now(),
    })
    try:
        from weasyprint import HTML
        pdf_file = io.BytesIO()
        HTML(string=html_string).write_pdf(pdf_file)
        pdf_file.seek(0)
        response = FileResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="participants_masterclass.pdf"'
        return response
    except Exception as e:
        return HttpResponse(f"Erreur PDF : {e}", status=500)

export_participants_pdf.short_description = "📄 Exporter la sélection en PDF"


# ─── Admin ─────────────────────────────────────────────────────────────────
@admin.register(Participant)
class ParticipantAdmin(ExportMixin, admin.ModelAdmin):
    resource_classes = [ParticipantResource]
    formats = [XLSX, CSV, PDFFormat]
    actions = [export_participants_pdf]

    list_display = (
        'ticket_badge',
        'nom_complet_display',
        'whatsapp',
        'etablissement',
        'created_at',
    )
    list_display_links = ('nom_complet_display',)
    search_fields = ('nom', 'prenom', 'whatsapp', 'ticket_number')
    list_filter = ('created_at',)
    readonly_fields = ('ticket_number', 'created_at')
    ordering = ('-created_at',)
    list_per_page = 25

    fieldsets = (
        ('Identité', {
            'fields': ('nom', 'prenom', 'whatsapp', 'etablissement'),
        }),
        ('Ticket & Inscription', {
            'fields': ('ticket_number', 'created_at'),
        }),
    )

    def get_export_filename(self, request, queryset, file_format):
        if isinstance(file_format, PDFFormat):
            return 'participants_masterclass.pdf'
        return super().get_export_filename(request, queryset, file_format)

    def get_export_data(self, file_format, request, queryset, **kwargs):
        """Intercepte l'export PDF pour passer le queryset au format."""
        if isinstance(file_format, PDFFormat):
            return file_format.export_data(None, queryset=queryset)
        return super().get_export_data(file_format, request, queryset, **kwargs)

    def nom_complet_display(self, obj):
        return f"{obj.prenom} {obj.nom}"
    nom_complet_display.short_description = "Nom complet"
    nom_complet_display.admin_order_field = 'nom'

    def ticket_badge(self, obj):
        return format_html(
            '<span style="'
            'background:#1d4ed8;color:#fff;padding:3px 8px;'
            'border-radius:4px;font-family:monospace;font-size:12px;">'
            '{}</span>',
            obj.ticket_number,
        )
    ticket_badge.short_description = "Ticket"
    ticket_badge.admin_order_field = 'ticket_number'


# Admin site customization
admin.site.site_header = "🎓 Masterclass – Administration"
admin.site.site_title = "Masterclass Admin"
admin.site.index_title = "Gestion des inscriptions"
