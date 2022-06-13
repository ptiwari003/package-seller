from django.urls import path
from .views import OrderGeneration, PdfView, CalculateTAkeRate, OrderList, render_pdf

urlpatterns = [
    path('pdf', PdfView.as_view(), name='pdf generation template' ),
    path('generate/pdf/<int:id>', render_pdf, name= 'order_specific_pdf'),
    path('calculate/takeRate', CalculateTAkeRate.as_view(), name='takerate_calculation' ),
    path('generate/order', OrderGeneration.as_view(), name='order_generation' ),
    path('list/orders', OrderList.as_view(), name='order_list')
]
