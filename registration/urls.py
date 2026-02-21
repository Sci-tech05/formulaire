from django.urls import path
from .views import InscriptionView, TicketPDFView

app_name = 'registration'

urlpatterns = [
    path('', InscriptionView.as_view(), name='inscription'),
    path('ticket/<str:ticket_number>/pdf/', TicketPDFView.as_view(), name='ticket_pdf'),
]
