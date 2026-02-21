from django import forms
from .models import Participant


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['nom', 'prenom', 'whatsapp', 'etablissement']
        widgets = {
            'nom': forms.TextInput(attrs={
                'placeholder': 'Ex : AGOSSA',
                'class': 'form-field',
                'autocomplete': 'family-name',
            }),
            'prenom': forms.TextInput(attrs={
                'placeholder': 'Ex : Kouamé',
                'class': 'form-field',
                'autocomplete': 'given-name',
            }),
            'whatsapp': forms.TextInput(attrs={
                'placeholder': 'Ex : +22967000000',
                'class': 'form-field',
                'type': 'tel',
                'autocomplete': 'tel',
            }),
            'etablissement': forms.TextInput(attrs={
                'placeholder': 'Ex : ENSET – Génie Électrique',
                'class': 'form-field',
            }),
        }
        labels = {
            'nom': 'Nom',
            'prenom': 'Prénom',
            'whatsapp': 'Numéro WhatsApp',
            'etablissement': 'Établissement / Filière (optionnel)',
        }

    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom', '').strip().lower()
        prenom = cleaned_data.get('prenom', '').strip().lower()

        if nom and prenom:
            if Participant.objects.filter(
                nom__iexact=nom,
                prenom__iexact=prenom
            ).exists():
                raise forms.ValidationError(
                    "Une inscription existe déjà pour "
                    f"« {prenom.capitalize()} {nom.upper()} ». "
                    "Une seule inscription par personne est autorisée."
                )
        return cleaned_data
