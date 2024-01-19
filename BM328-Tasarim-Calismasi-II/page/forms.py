from django import forms
from .models import Carousel, Page


class CarouselModelForm(forms.ModelForm) :
    class Meta:
        model = Carousel
        fields = [
            'title',
            'cover_image',
            'status',
        ]      
        
class PageModelForm(forms.ModelForm):
    class Meta:
        model = Page
        # fields = '__all__'        bütün sütunları al
        # exclude = ['title']       title hariç bütün alanları al
        fields = [                  # istenilenleri getir
            'title',
            'cover_image',
            'content',
            'status',
        ]