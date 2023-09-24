from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

# Create your views here.



class InvoiceListCreateView(generics.ListCreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


class InvoiceDetailListCreateView(generics.ListCreateAPIView):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InvoiceDetail.objects.all()
    serializer_class = InvoiceDetailSerializer




class InvoiceAndDetailAPIView(APIView):
    def get(self, request, *args, **kwargs):
        invoices = Invoice.objects.all()
        invoice_details = InvoiceDetail.objects.all()

        invoice_serializer = InvoiceSerializer(invoices, many=True)
        detail_serializer = InvoiceDetailSerializer(invoice_details, many=True)

        return Response({
            'invoices': invoice_serializer.data,
            'invoice_details': detail_serializer.data
        })

    def post(self, request, *args, **kwargs):
        invoice_serializer = InvoiceSerializer(data=request.data.get('invoice'))
        detail_serializer = InvoiceDetailSerializer(data=request.data.get('invoice_detail'))

        if invoice_serializer.is_valid() and detail_serializer.is_valid():
            invoice = invoice_serializer.save()
            detail_serializer.save(invoice=invoice)
            return Response({'message': 'Invoice and InvoiceDetail created successfully'},
                            status=status.HTTP_201_CREATED)
        else:
            errors = {
                'invoice_errors': invoice_serializer.errors,
                'detail_errors': detail_serializer.errors
            }
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):

        invoice_data = request.data.get('invoice')
        detail_data = request.data.get('invoice_detail')

        if invoice_data and detail_data:
            invoice = Invoice.objects.get(pk=invoice_data['id'])
            invoice_serializer = InvoiceSerializer(instance=invoice, data=invoice_data)
            if invoice_serializer.is_valid():
                invoice_serializer.save()

            detail = InvoiceDetail.objects.get(pk=detail_data['id'])
            detail_serializer = InvoiceDetailSerializer(instance=detail, data=detail_data)
            if detail_serializer.is_valid():
                detail_serializer.save()

            return Response({'message': 'Invoice and InvoiceDetail updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Both invoice and invoice_detail data are required'}, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        # Handle PATCH requests to partially update invoices and details
        invoice_data = request.data.get('invoice')
        detail_data = request.data.get('invoice_detail')

        if invoice_data:
            invoice = Invoice.objects.get(pk=invoice_data['id'])
            invoice_serializer = InvoiceSerializer(instance=invoice, data=invoice_data, partial=True)
            if invoice_serializer.is_valid():
                invoice_serializer.save()

        if detail_data:
            detail = InvoiceDetail.objects.get(pk=detail_data['id'])
            detail_serializer = InvoiceDetailSerializer(instance=detail, data=detail_data, partial=True)
            if detail_serializer.is_valid():
                detail_serializer.save()

        return Response({'message': 'Invoice and InvoiceDetail partially updated successfully'}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Handle DELETE requests to delete invoices and details
        invoice_id = request.data.get('invoice_id')
        detail_id = request.data.get('invoice_detail_id')

        if invoice_id:
            try:
                invoice = Invoice.objects.get(pk=invoice_id)
                invoice.delete()
            except Invoice.DoesNotExist:
                pass

        if detail_id:
            try:
                detail = InvoiceDetail.objects.get(pk=detail_id)
                detail.delete()
            except InvoiceDetail.DoesNotExist:
                pass

        return Response({'message': 'Invoice and InvoiceDetail deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


