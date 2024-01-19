from django.contrib import admin
from .models import Page, Carousel

# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 
        'title',
        'status',
        'slug',
        'updated_at',
    )
    list_filter = (
        'status',
    )


class CarouselAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 
        'title',
        'cover_image',
        'status',
    )
    list_filter = (
        'status',
    )
    list_editable = list_filter

admin.site.register(Page, PageAdmin) 
admin.site.register(Carousel, CarouselAdmin)