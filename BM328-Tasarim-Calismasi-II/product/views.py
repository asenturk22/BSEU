from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import (
    Category, 
    Product,
    Order,
    OrderItem,
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist


STATUS = "published"

def category_show(request, category_slug):
    context = dict()
    context['category'] = get_object_or_404(Category, slug=category_slug)
    #Nav:
    # context['categories'] = Category.objects.filter(
    #     status=STATUS,
    # )
    context["items"] = Product.objects.filter(
        category=context['category'],
        status=STATUS,
        stock__gte=1,
    )
    return render(request, "product/category_show.html", context)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            current_order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object':current_order
            }
            return render(self.request, 'product/summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'Yeni bir siparişiniz yok.')
            return redirect('/')
        
        return render(self.request, 'product/summary.html', context)  


@login_required(login_url='..accounts/login/')
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered = False,
    )

    order_q = Order.objects.filter(user=request.user, ordered=False)
    if order_q.exists():
        order = order_q[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Ürün sepete eklendi")
            return redirect("product:summary")
        else:
            messages.info(request, "Ürün sepete eklendi")
            order.items.add(order_item)
            return redirect("product:summary")
    else:
        ordered_date = timezone.now() 
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "sepete eklendi")
        order.items.add(order_item)
        return redirect("product:summary")
        
      

@login_required(login_url='..accounts/login/')
def remove_single_item(request, slug):
    item = get_object_or_404(Product, slug=slug)

    order_q = Order.objects.filter(user=request.user, ordered=False)
    if order_q.exists():
        order = order_q[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if (order_item.quantity > 1):
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request, "Sepet güncellendi")
            return redirect("product:summary")
        else:
            messages.info(request, "Ürün sepetinizde yok")
            return redirect("product:detail")
    else:
        messages.info(request, "aktif bir sipariniz yok")
        return redirect("product:detail", slug=slug)
      

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "Sepetten ürün silindi")
            return redirect("product:summary")
        else:
            # you can add a message saying the order does not contain the item
            messages.info(request, "Bu ürün sepetinizde yok")
            return redirect("product:sumary")

    else:
        # add a message, no order
        messages.info(request, "Etkin bir siparişiniz yok")
        return redirect("product:sumary")
    

