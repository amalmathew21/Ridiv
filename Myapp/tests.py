from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.db.models import Max
from .models import Invoice, InvoiceDetail
import json

from .serializers import InvoiceSerializer, InvoiceDetailSerializer


class InvoiceTestCase(APITestCase):
    # Creating invoice
    def setUp(self):
        self.invoice_data = {
            "date": "2023-09-30",
            "customer_name": "Jio Company",
        }

        self.invoice_details_data = [
            {
                "description": "Product A",
                "quantity": 5,
                "unit_price": "10.0",
                "price": "50.0"
            },
            {
                "description": "Product B",
                "quantity": 3,
                "unit_price": "8.0",
                "price": "24.0"
            }
        ]

    def test_create_invoice(self):
        url = reverse('invoice-list-create')
        response = self.client.post(url, json.dumps(self.invoice_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)

        invoice = Invoice.objects.first()
        self.assertEqual(invoice.customer_name, "Jio Company")

    def test_create_invoice_details(self):

        invoice_url = reverse('invoice-list-create')
        response = self.client.post(invoice_url, json.dumps(self.invoice_data), content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)


        invoice = Invoice.objects.first()
        invoice_id = invoice.id

        details_url = reverse('invoice-detail-list-create')
        for detail_data in self.invoice_details_data:
            detail_data["invoice"] = invoice_id
            response = self.client.post(details_url, json.dumps(detail_data), content_type='application/json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        invoice_details_count = InvoiceDetail.objects.filter(invoice=invoice).count()
        self.assertEqual(invoice_details_count, 2)

    # Updating Invoice
    def test_update_invoice(self):
        invoice = Invoice.objects.create(date="2023-09-30", customer_name="Jio Company")
        url = reverse('invoice-details', args=[invoice.id])
        data = {
            "date": "2023-09-29",
            "customer_name": "XYZ Corporation"
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_invoice = Invoice.objects.get(id=invoice.id)
        self.assertEqual(updated_invoice.customer_name, "XYZ Corporation")


class InvoiceDetailAPITestCase(APITestCase):
    # Creating Invoice detail
    def test_create_invoice_detail(self):
        invoice = Invoice.objects.create(date="2023-09-25", customer_name="Ridiv Company")
        url = reverse('invoice-detail-list-create')
        data = {
            "invoice": invoice.id,
            "description": "Product Ridiv",
            "quantity": 8,
            "unit_price": 100.0,
            "price": 800.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

    # Updating invoice detail
    def test_update_invoice_detail(self):
        invoice = Invoice.objects.create(date="2023-09-25", customer_name="Ridiv Company")
        invoice_detail = InvoiceDetail.objects.create(invoice=invoice, description="Product Ridiv", quantity=8,
                                                      unit_price=100.0, price=800.0)
        url = reverse('invoice-detail-data', args=[invoice_detail.id])
        data = {
            "invoice": invoice.id,
            "description": "Updated Product Ridiv",
            "quantity": 10,
            "unit_price": 200.0,
            "price": 200.0
        }
        response = self.client.put(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_detail = InvoiceDetail.objects.get(id=invoice_detail.id)
        self.assertEqual(updated_detail.description, "Updated Product Ridiv")

    # Retrieve all Invoice
    def test_list_invoice_details(self):
        invoice = Invoice.objects.create(date="2023-09-27", customer_name="ABC Company")
        InvoiceDetail.objects.create(invoice=invoice, description="Product A", quantity=5, unit_price=10.0, price=50.0)
        InvoiceDetail.objects.create(invoice=invoice, description="Product B", quantity=3, unit_price=8.0, price=24.0)

        url = reverse('invoice-detail-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # Retrieve single
    def test_retrieve_invoice_detail(self):
        invoice = Invoice.objects.create(date="2023-09-28", customer_name="KLM Company")
        invoice_detail = InvoiceDetail.objects.create(invoice=invoice, description="Product Q", quantity=15, unit_price=10.0,
                                                      price=150.0)

        url = reverse('invoice-detail-data', args=[invoice_detail.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['description'], "Product Q")

    # Update
    def test_partial_update_invoice_detail(self):
        invoice = Invoice.objects.create(date="2023-09-26", customer_name="ZYX Company")
        invoice_detail = InvoiceDetail.objects.create(invoice=invoice, description="Product K", quantity=25,
                                                      unit_price=10.0,
                                                      price=250.0)
        url = reverse('invoice-detail-data', args=[invoice_detail.id])
        data = {
            "description": "Updated Product K"
        }
        response = self.client.patch(url, json.dumps(data), content_type='application/json')  # Use PATCH request
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_detail = InvoiceDetail.objects.get(id=invoice_detail.id)
        self.assertEqual(updated_detail.description, "Updated Product K")

    # Delete Invoice Detail
    def test_delete_invoice_detail(self):
        invoice = Invoice.objects.create(date="2023-09-15", customer_name="ABC Company")
        invoice_detail = InvoiceDetail.objects.create(invoice=invoice, description="Product A", quantity=10, unit_price=10.0,
                                                      price=100.0)
        url = reverse('invoice-detail-data', args=[invoice_detail.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)







# class InvoiceAPITestCase(APITestCase):
#
#     def test_create_invoice_and_detail(self):
#         url = reverse('invoice-and-detail')
#
#         data = {
#             "date": "2023-09-30",
#             "customer_name": "Jio Company",
#             "details": [
#                 {
#                     "description": "Product A",
#                     "quantity": 5,
#                     "unit_price": "10.0",
#                     "price": "50.0"
#                 }
#             ]
#         }
#
#         # Create serializers and validate the data
#         serializer = InvoiceSerializer(data=data)
#         detail_serializer = InvoiceDetailSerializer(data=data['details'], many=True)
#
#         self.assertTrue(serializer.is_valid())
#         self.assertTrue(detail_serializer.is_valid())
#
#         # Save the data only if it's valid
#         if serializer.is_valid() and detail_serializer.is_valid():
#             serializer.save()
#             for detail_data in data['details']:
#                 detail_serializer.save(invoice=serializer.instance)
#
#         response = self.client.post(url, json.dumps(data), content_type='application/json')
#
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#
#         # Verify that the invoice and detail were created
#         self.assertEqual(Invoice.objects.count(), 1)
#         self.assertEqual(InvoiceDetail.objects.count(), 1)
#
#         # Retrieve the created invoice and detail
#         invoice = Invoice.objects.first()
#         detail = InvoiceDetail.objects.first()
#
#         self.assertEqual(invoice.customer_name, "Jio Company")
#         self.assertEqual(detail.description, "Product A")
#
#     def test_update_invoice(self):
#         invoice = Invoice.objects.create(date="2023-09-26", customer_name="KJI Company")
#         invoice_detail = InvoiceDetail.objects.create(invoice=invoice, description="Product J", quantity=25,
#                                                       unit_price=10.0,
#                                                       price=250.0)
#         url = reverse('invoice-and-detail', args=[invoice_detail.id])
#         data = {
#             "date": "2023-09-29",
#             "customer_name": "XYZ Corporation"
#         }
#         response = self.client.put(url, json.dumps(data), content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_detail = InvoiceDetail.objects.get(id=invoice_detail.id)
#         self.assertEqual(updated_detail.description, "Updated Product J")
#
#     def test_partial_update_invoice(self):
#         invoice = Invoice.objects.create(date="2023-09-29", customer_name="Jio Company")
#         url = reverse('invoice-and-detail', args=[invoice.id])
#         data = {
#             "date": "2023-09-30"
#         }
#         response = self.client.patch(url, json.dumps(data), content_type='application/json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         updated_invoice = Invoice.objects.get(id=invoice.id)
#         self.assertEqual(updated_invoice.date.strftime('%Y-%m-%d'), "2023-09-30")
#
#     def test_delete_invoice_and_detail(self):
#         invoice = Invoice.objects.create(date="2023-09-30", customer_name="Jio Company")
#         detail = InvoiceDetail.objects.create(
#             invoice=invoice, description="Product A", quantity=5, unit_price="10.0", price="50.0"
#         )
#
#         url = reverse('invoice-and-detail', args=[invoice.id])
#         data = {
#             "invoice_id": invoice.id,
#             "invoice_detail_id": detail.id
#         }
#         response = self.client.delete(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertFalse(Invoice.objects.filter(id=invoice.id).exists())
#         self.assertFalse(InvoiceDetail.objects.filter(id=detail.id).exists())
