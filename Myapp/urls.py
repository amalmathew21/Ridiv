from django.urls import path
from . import views
from .views import InvoiceAndDetailAPIView

urlpatterns = [
    path('invoiceslist/', views.InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoiceslist/<int:pk>/', views.InvoiceView.as_view(), name='invoice-details'),
    path('invoice-details/', views.InvoiceDetailListCreateView.as_view(), name='invoice-detail-list-create'),
    path('invoice-details/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice-detail-data'),


    path('invoices/', views.InvoiceAndDetailAPIView.as_view(), name='invoice-and-detail'),
    path('invoices/<int:pk>/', views.InvoiceAndDetailAPIView.as_view(), name='invoice-and-detail'),

]
