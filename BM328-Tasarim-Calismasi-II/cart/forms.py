from django import forms
from django.core import validators
from tinymce.widgets import TinyMCE
from product.models import (
    BillingAddress, 
    Coupon,
    #Cities
)


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Coupon code'
    }))
    



class ShippingAddressForm(forms.ModelForm):
    address_text = forms.CharField(widget=forms.Textarea(
        attrs={'rows':5, 'cols':25}), label="Adres")

    class Meta:
        model = BillingAddress
        fields = [
            'country',
            'city',
            'town',
            'district',
            'postal_code',
            'address_text'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['city'].queryset = Cities.objects.none()
        #self.fields['town'].queryset = Cities.objects.none()
        #self.fields['district'].queryset = Cities.objects.none()
        




