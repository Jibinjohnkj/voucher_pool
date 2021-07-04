import datetime


from .models import Customer, Offer, Voucher
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):

    class Meta:

        model = Customer
        fields = ['first_name', 'last_name', 'email']


class OfferSerializer(serializers.ModelSerializer):

    class Meta:

        model = Offer
        fields = ['name', 'discount']


class VoucherSerializer(serializers.ModelSerializer):
    offer = serializers.ReadOnlyField(source='offer.name')

    class Meta:

        model = Voucher
        fields = ['code', 'offer']


class OfferField(serializers.RelatedField):
    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        return data

class GenerateVoucherSerializer(serializers.ModelSerializer):
    offer = OfferField(source='offer.name', queryset=Offer.objects.all())

    class Meta:

        model = Voucher
        fields = ['offer', 'expiration']
