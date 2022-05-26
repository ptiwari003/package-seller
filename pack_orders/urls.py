from django.urls import path
from .views import PdfView

urlpatterns = [
    path('pdf', PdfView.as_view(), name='pdf generation template' )
]
