from django.urls import path
from .views import (
    ShippingAddressView,
    addCouponView,
    PaymentView,
)

app_name = 'cart'

urlpatterns = [
    path('address/', ShippingAddressView.as_view() , name='address'),
    path('add-coupon/', addCouponView.as_view() , name='add-coupon'),
    path('payment/', PaymentView.as_view(), name='payment'  )
]

