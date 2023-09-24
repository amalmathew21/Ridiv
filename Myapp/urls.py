from django.urls import path
from . import views

urlpatterns = [
    path('invoices/', views.InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', views.InvoiceView.as_view(), name='invoice-details'),
    path('invoice-details/', views.InvoiceDetailListCreateView.as_view(), name='invoice-detail-list-create'),
    path('invoice-details/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail-data'),
]
