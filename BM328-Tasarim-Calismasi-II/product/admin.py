from django.contrib import admin
from .models import (
    Category,
    Countries, Cities, Towns, Districts, BillingAddress,
    Product,
    OrderItem, 
    Order,
    Coupon,
    Payments,
    Refund,
)


def change_refund_to_granted(modelAdmin, request, queryset):
    queryset.update(refund_granted=True)


def change_to_delivered(modelAdmin, request, queryset):
    queryset.update(delivered=True, received=True)

class SnippetOrderAdmin(admin.ModelAdmin):
    list_display = [
        'user', 
        'ordered',
        'delivered',
        'refund_requested',
        'refund_granted',
        'billing_address',
        'payment',
        'coupon',
    ]

    list_display_links = [
        'user', 
        'billing_address',
        'payment',
        'coupon',
    ]
    
    actions = [
        change_refund_to_granted,
        change_to_delivered,
    ]
    



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = (
        'pk',
        'title',
        'slug',
        'gender',
        'status',
        'updated_at',
    )
    list_filter = (
        'status',
        'gender',
    )
    list_editable = (
        'title',
        'status',
    )
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ('title',)}
    list_display = (
        'pk',
        'title',
        'price', 
        'stock',
        'is_home',
        'cover_image',
        'slug',
        'status',
        'updated_at',
    )
    list_filter = (
        'status',
    )
    list_editable = (
        'is_home',
        'title',
        'status',
    )


admin.site.register(Order, SnippetOrderAdmin)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Countries)
class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'country',
    )


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'country_id',
        'city',
    )
    list_filter = (
        'country_id',
    )


@admin.register(Towns)
class TownsAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'town',
    )


@admin.register(Districts)
class DistrictsAdmin(admin.ModelAdmin):
    pass


@admin.register(BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    pass


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    pass
