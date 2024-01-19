from django.shortcuts import render,redirect, get_list_or_404
from django.views.generic import  ListView, DetailView, View
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse, HttpResponse
from product.models import (
    Order,
    BillingAddress,
    Coupon,
    Payments,
    Cities,
)
import json
from .forms import (
    ShippingAddressForm,
    CouponForm,
)

import stripe
import random
import string
import config

stripe.api_key = config.settings.STRIPE_SECRET_KEY

def create_order_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

#@login_required(login_url='accounts:login_view')
class ShippingAddressView(LoginRequiredMixin, View):
    def get(self,*args, **kwargs):
        try:
            order = Order.objects.get(
                user=self.request.user, 
                ordered=False
            )
            form = ShippingAddressForm()
            couponform = CouponForm()
            context = dict(
                form=form,
                order=order,
                couponform=couponform,
                display_coupon_form=True,
            )
            context['title'] = "Adres Bilgilerini Getir"
            if self.request.method == 'POST':
                form = ShippingAddressForm(self.request.POST or None, self.request.FILES or None)    
                if form.is_valid():
                    f = form.save(commit=False)
                    f.user = self.request.user
                    f.save()
            context = dict(
                form=form,
                order=order,
                couponform=couponform,
                display_coupon_form=True,
            )
            return render(self.request, 'cart/shipping_address.html', context)
        except ObjectDoesNotExist:
            messages.info(self.request, 'Aktif siparişiniz yok')
            return redirect('product:summary')
        
    def post(self, *args, **kwargs):
        try:
            form = ShippingAddressForm(self.request.POST or None)
            order = Order.objects.get(
                user=self.request.user, 
                ordered=False
            ) 
            if form.is_valid():
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                town = form.cleaned_data.get('town')
                district = form.cleaned_data.get('district')
                postal_code = form.cleaned_data.get('postal_code')
                address_text = form.cleaned_data.get('address_text')

                billing_address = BillingAddress(
                    user=self.request.user,
                    country=country,
                    city=city,
                    town=town,
                    district=district,
                    postal_code=postal_code,
                    address_text=address_text
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()

                messages.info(self.request, 'Sipariş adresiniz eklendi')
                return redirect('cart:payment')
        except ObjectDoesNotExist:
            messages.info(self.request, 'Aktif siparişiniz yok')
            return redirect('product:summary')
    

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, 'Bu kupon geçerli değildir.')
        return redirect('product:summary')


class addCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get('code')
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, 'Coupon eklendi')
                return redirect('cart:address')
            except ObjectDoesNotExist:
                messages.success(self.request, "Geçerli bir siparişiniz yok")
                return redirect('product:summary')
            

class PaymentView(View):
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'display_coupon_form' : False,
            }
            return render(self.request, 'cart/payment.html', context)
        else:
            messages.warning(self.request, 'Lütfen bir adres ekleyin')
            return redirect('cart:address')

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.total_price() * 100)
        print("-"*100)
        #print(stripe.Customer.list())
        print(token)
        print(amount)
        print("-"*100)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                source=token,
                description='DjangoE-Trade Ödeme'
            ) 
            #print(charge)
            print("-"*100)
            payment = Payments()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.total_price()

            print("="*100)
            print("payment:", payment)
            print(payment.stripe_charge_id)
            print(payment.user)
            print(payment.amount)
            print("="*100)

            order_items = order.items.all()
            order_items.update(ordered=True)

            for item in order_items: 
                item.save()

            order.ordered = True
            order.payment = payment

            order.order_ref = create_order_code()
            payment.save()
            order.save()

            messages.success(self.request, 'Siparişiniz alındı')
            return redirect('/')

        except stripe.error.CardError as e :
            body = e.json_body
            err = body.get('error', {})
            messages.warning(self.request, f"{err.get('message')}")
            return redirect('cart:payment')
        except stripe.error.RateLimitError as e : 
            messages.warning(self.request, 'Rate Limit Error')
            return redirect('cart:payment')
        except stripe.error.InvalidRequestError as e : 
            messages.warning(self.request, 'Geçersiz parametre')
            print('invalid parameters', e)
            print('the value is ', amount)
            return redirect('cart:payment')
        except stripe.error.AuthenticationError as e : 
            messages.warning(self.request, 'Not authenticated')
            return redirect('cart:payment')
        except stripe.error.APIConnectionError as e : 
            messages.warning(self.request, 'Network Error')
            return redirect('cart:payment')
        except stripe.error.StripeError as e : 
            messages.warning(self.request, 'Something went wong, you were not charged, please try again!')
            return redirect('cart:payment')
        except Exception as e :
            messages.warning(self.request, 'Something went wong, we will work about it since we have been notified')
            return redirect('cart:payment')



