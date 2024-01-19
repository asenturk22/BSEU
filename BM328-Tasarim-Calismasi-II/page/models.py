from django.db import models
#from django.contrib.auth.models import User
from autoslug import AutoSlugField

# Third Party Apps:
from django.urls import reverse
from tinymce import models as tinymce_models

DEFAULT_STATUS = "draft"

STATUS = [
    ('draft', 'Taslak'),
    ('published', 'Yayinlandi'),
    ('deleted', 'Silindi'),
]

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title', unique=True, default="")
    content = tinymce_models.HTMLField(blank=True, null=True)
    cover_image = models.ImageField(
        upload_to='page',
        null=True,
        blank=True,
    )
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_Active = models.BooleanField(default=False)

    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self): 
        return self.title

    def get_absolute_url(self):
        return reverse(
            'page:page_view',
            kwargs={
                'page_slug':self.slug,
            }
        )
    

class Carousel(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    cover_image = models.ImageField(
        upload_to="carousel",
        null=True,
        blank=True,
    )
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    ) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
