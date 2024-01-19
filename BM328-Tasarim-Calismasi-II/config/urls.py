from django.contrib import admin
from django.urls import path, include
from page.views import home
from django.conf import settings
from django.conf.urls.static import static
from product.views import category_show

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('accounts.urls', namespace='user'),),
    path('cart/', include('cart.urls'), ), 
    path('product/', include('product.urls'), ), 
    path('', include('page.urls'),), 
    path('<slug:category_slug>', category_show, name="category_show"),
] + static( 
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
