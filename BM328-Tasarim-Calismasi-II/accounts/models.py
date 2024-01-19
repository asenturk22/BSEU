from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField

GENDER_CHOICE = [
    ('E', 'Erkek'),
    ('K', 'Kadin'),
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatar')
    instagram = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)

