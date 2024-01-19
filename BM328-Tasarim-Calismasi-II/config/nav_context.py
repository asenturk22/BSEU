from product.models import Category
from page.models import Page
from page.views import STATUS
#from product.models import Order


def nav_data(request):
    context = dict()
    context['categories'] = Category.objects.filter(
        status=STATUS,
    ).order_by('title')
    context['pages'] = Page.objects.filter(
        status=STATUS,
    ).order_by('title')
    return context 



# def cart_count(request):
#     if request.user.is_authenticated:
#         query_set = Order.object.filter(user=request.user, ordered=False)
#         if query_set.exists():
#             return query_set[0].items.count()
#         return 0