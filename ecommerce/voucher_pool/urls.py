from django.urls import path

from .views import CustomerList, OfferList, GenerateVoucher, GetDiscount, VoucherList

urlpatterns = [
    path('voucher/', VoucherList.as_view(), name ='voucher'),
    path('generate_vouchers/', GenerateVoucher.as_view(), name='generate-vouchers'),
    path('discount/', GetDiscount.as_view(), name='get-discount'),
    path('customer/', CustomerList.as_view(), name='customer-list-create'),
    path('offer/', OfferList.as_view(), name='offer-list-create')
]