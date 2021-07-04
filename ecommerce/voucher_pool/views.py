from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.utils.http import urlencode
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from distutils.util import strtobool

from .serializers import CustomerSerializer, OfferSerializer, VoucherSerializer, GenerateVoucherSerializer
from .models import Customer, Offer, Voucher


class CustomerList(generics.ListCreateAPIView):
    """
    GET:
    Returns all customers in the system

    POST:
    Creates a new customer
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

class OfferList(generics.ListCreateAPIView):
    """
    GET:
    Returns all offers in the system

    POST:
    Creates a new offer
    """
    serializer_class = OfferSerializer
    queryset = Offer.objects.all()


class GenerateVoucher(APIView):
    """
    POST:
    Creates a voucher for all customers for the given offer and expiration date
    """
    serializer_class = GenerateVoucherSerializer
    def post(self, request):
        offer = self.request.data.get('offer')
        expiration = self.request.data.get('expiration')

        if offer.isnumeric():
            offer = Offer.objects.get(id=int(offer))
        else:
            offer = Offer.objects.get(name=offer)
        for customer in Customer.objects.all():
            voucher = Voucher(customer=customer,offer=offer,expiration=expiration)
            voucher.save()

        queryset = Voucher.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class VoucherList(APIView):
    """
    GET:
    Returns all valid vocuhers in the system for the given user
    """
    serializer_class = VoucherSerializer
    def get_queryset(self):
        queryset = Voucher.objects.all()
        expired = self.request.query_params.get('expired', 'false')
        email = self.request.query_params.get('email')
        if email:
           queryset = queryset.filter(customer__email=email)
        if not strtobool(expired):
           queryset = queryset.filter(used_on__isnull=True)
        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetDiscount(APIView):
    """
    GET:
    Validate the voucher, mark it as used and return discount
    """
    serializer_class = VoucherSerializer
    def get_object(self):
        email = self.request.query_params.get('email')
        code = self.request.query_params.get('code')
        voucher = get_object_or_404(Voucher, customer__email=email, code=code, used_on__isnull=True)
        return voucher

    def get(self, request):
        voucher = self.get_object()
        voucher.used_on = now()
        voucher.save()
        return Response(voucher.offer.discount)


