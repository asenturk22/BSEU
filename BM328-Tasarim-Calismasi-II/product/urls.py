from django.urls import path
from .views import (
    ProductDetailView,
    add_to_cart,
    remove_single_item,
    remove_from_cart,
    OrderSummaryView
)

app_name = 'product'

urlpatterns = [
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add_to_cart' ),
    path('remove_single_item/<slug:slug>', remove_single_item, name="remove_single_item"),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
    path('summary/', OrderSummaryView.as_view(), name='summary'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='detail'),
]