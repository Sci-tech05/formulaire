from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import FileResponse, HttpResponse
from django.conf import settings
from django.contrib import messages
import io

from .forms import ParticipantForm
from .models import Participant

MAX_PLACES = getattr(settings, 'EVENT_MAX_PLACES', 100)


def get_places_context():
    """Retourne le contexte commun : places restantes, compteur."""
    inscrits = Participant.objects.count()
    places_restantes = max(0, MAX_PLACES - inscrits)
    inscrits_percent = round((inscrits / MAX_PLACES) * 100) if MAX_PLACES > 0 else 0
    return {
        'inscrits': inscrits,
        'inscrits_percent': inscrits_percent,
        'places_restantes': places_restantes,
        'max_places': MAX_PLACES,
        'inscriptions_closes': inscrits >= MAX_PLACES,
        'event_title': settings.EVENT_TITLE,
        'event_date': settings.EVENT_DATE,
        'event_heure': settings.EVENT_HEURE,
        'event_lieu': settings.EVENT_LIEU,
    }


class InscriptionView(View):
    """Vue principale : formulaire d'inscription."""
    template_name = 'inscription.html'

    def get(self, request):
        ctx = get_places_context()
        if ctx['inscriptions_closes']:
            ctx['form'] = None
        else:
            ctx['form'] = ParticipantForm()
        return render(request, self.template_name, ctx)

    def post(self, request):
        ctx = get_places_context()

        if ctx['inscriptions_closes']:
            messages.error(
                request,
                "Les inscriptions sont closes — 100 places atteintes. "
                "Merci pour votre intérêt !"
            )
            ctx['form'] = None
            return render(request, self.template_name, ctx)

        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(
                request,
                f"Inscription réussie ! Ton ticket est prêt, {participant.prenom} 🎉"
            )
            ctx.update(get_places_context())  # re-count after save
            ctx['participant'] = participant
            ctx['form'] = ParticipantForm()  # reset form

            # Lien WhatsApp pré-rempli (bonus)
            wa_text = (
                f"Bonjour {participant.prenom} ! "
                f"Merci pour ton inscription à la Masterclass Étudiant Entrepreneur. "
                f"Ton ticket : {participant.ticket_number}. "
                f"RDV le {settings.EVENT_DATE} à {settings.EVENT_HEURE} – {settings.EVENT_LIEU}. "
                f"Télécharge ton ticket ici. À bientôt !"
            )
            import urllib.parse
            wa_number = participant.whatsapp.replace('+', '').replace(' ', '')
            ctx['whatsapp_link'] = (
                f"https://wa.me/{wa_number}?text={urllib.parse.quote(wa_text)}"
            )
            ctx['pdf_url'] = f"/ticket/{participant.ticket_number}/pdf/"
            return render(request, self.template_name, ctx)

        ctx['form'] = form
        return render(request, self.template_name, ctx)


class TicketPDFView(View):
    """Génère et sert le ticket en PDF via WeasyPrint."""

    def get(self, request, ticket_number):
        participant = get_object_or_404(Participant, ticket_number=ticket_number)

        # Render HTML template to string
        from django.template.loader import render_to_string
        html_string = render_to_string('ticket_pdf.html', {
            'participant': participant,
            'event_title': settings.EVENT_TITLE,
            'event_date': settings.EVENT_DATE,
            'event_heure': settings.EVENT_HEURE,
            'event_lieu': settings.EVENT_LIEU,
        }, request=request)

        try:
            from weasyprint import HTML, CSS
            pdf_file = io.BytesIO()
            HTML(string=html_string, base_url=request.build_absolute_uri('/')).write_pdf(pdf_file)
            pdf_file.seek(0)
            filename = f"ticket_{participant.ticket_number}.pdf"
            response = FileResponse(
                pdf_file,
                content_type='application/pdf',
            )
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except ImportError:
            return HttpResponse(
                "<h2>WeasyPrint non installé.</h2>"
                "<p>Installez-le avec : <code>pip install weasyprint</code></p>",
                status=500
            )
        except Exception as e:
            return HttpResponse(
                f"<h2>Erreur PDF</h2><pre>{e}</pre>",
                status=500
            )
