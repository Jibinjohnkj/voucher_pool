from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Customer, Offer, Voucher

class CustomerTests(APITestCase):

    def test_create_customer(self):
        """
        Ensure we can create a new customer object.
        """
        url = reverse('customer-list-create')
        data = {'first_name': 'Test',
                'last_name': 'user',
                'email': 'testuser@gmail.com'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 1)
        self.assertEqual(Customer.objects.get().email, 'testuser@gmail.com')

class OfferTests(APITestCase):

    def test_create_offer(self):
        """
        Ensure we can create a new offer object.
        """
        url = reverse('offer-list-create')
        data = {'name': 'TestOffer',
                'discount': '50'
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Offer.objects.count(), 1)
        self.assertEqual(Offer.objects.get().name, 'TestOffer')

class VoucherTests1(APITestCase):

    def setUp(self):
        Customer.objects.create(first_name="Test", last_name="user", email="testuser@gmail.com")
        Offer.objects.create(name="TestOffer", discount="50")

        customer = Customer.objects.create(first_name="Test", last_name="user2", email="testuser2@gmail.com")
        offer = Offer.objects.create(name="TestOffer2", discount="20")
        Voucher.objects.create(customer=customer, offer=offer, expiration="2032-01-01")

    def test_generate_voucher(self):
        """
        Ensure new voucher objects are created for evey customer
        """
        url = reverse('generate-vouchers')
        data = {'offer': 'TestOffer',
                "expiration":"2032-01-01"
                }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        testoffer = Voucher.objects.filter(offer__name='TestOffer')
        self.assertEqual(testoffer.count(), 2)

class VoucherTests2(APITestCase):
    def setUp(self):
        customer = Customer.objects.create(first_name="Test", last_name="user", email="testuser@gmail.com")
        offer = Offer.objects.create(name="TestOffer", discount="50")
        Voucher.objects.create(customer=customer, offer=offer, expiration="2032-01-01")

    def test_voucher_list(self):
        """
        Ensure all valid vouchers for given customer are returned
        """
        url = reverse('voucher')
        email = 'testuser@gmail.com'
        url = "{0}?email={1}".format(url, email)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.pop()
        self.assertDictContainsSubset({'offer': 'TestOffer'},data)
        self.assertTrue('code' in data)

    def test_discount(self):
        """
        Ensure voucher is marked as used and discount is returned
        """
        url = reverse('get-discount')
        email = 'testuser@gmail.com'
        code = Voucher.objects.get().code
        url = "{0}?code={1}&email={2}".format(url, code, email)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, 50)

        valid_voucher = Voucher.objects.filter(used_on__isnull = True)
        empty_voucher_queryset = Voucher.objects.none()
        self.assertQuerysetEqual(valid_voucher, empty_voucher_queryset)

    def test_invalid_voucher(self):
        """
        Ensure voucher cannot be repeatedly used
        """
        url = reverse('get-discount')
        email = 'testuser@gmail.com'
        code = Voucher.objects.get().code
        url = "{0}?code={1}&email={2}".format(url, code, email)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        url = "{0}?code={1}&email={2}".format(url, code, email)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

