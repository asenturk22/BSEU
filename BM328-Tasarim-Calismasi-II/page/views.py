from django.shortcuts import render, redirect, get_object_or_404
from page.models import Page
from .models import Carousel
from django.contrib import messages
from django.utils.text import slugify
from .forms import CarouselModelForm, PageModelForm
from product.models import Product
from django.contrib.admin.views.decorators import staff_member_required

STATUS = "published"

# User : 
def home(request):
    context = dict()
    context['images'] = Carousel.objects.filter(
        status=STATUS
    ).exclude(cover_image='')

    products = Product.objects.filter(
        is_home=True,
        status=STATUS, 
    )
    
    context['products'] = products
    print(products)

    return render(request, 'page/index.html', context)


def page_show(request, slug) : 
    context = dict()
    page = get_object_or_404(Page, slug=slug)
    context['page'] = page
    return render(request, "page/page.html", context)



def manage_list(request):
    context = dict()
    return render(request, "manage/manage.html", context)


@staff_member_required
def page_list(request):
    context = dict()
    context['items'] = Page.objects.all().order_by('-pk')
    return render(request, "manage/page_list.html", context)


def page_create(request):
    context = dict()
    context['title'] = "Page Create Form"
    context['form'] = PageModelForm()

    #item = Carousel.objects.first()
    #context['form'] = CarouselModelForm(instance=item)

    if request.method == 'POST':
        form = PageModelForm(request.POST, request.FILES)
        print(form)
        if form.is_valid() :
            item = form.save(commit=False)
            item.slug = slugify(item.title.replace('ı', 'i'))
            form.save()
            messages.success(request, "successfull")
    return render(request, "manage/form.html", context)


def page_update(request, pk):
    context = dict()
    item = Page.objects.get(pk=pk)
    context['title'] = f"{item.title} - Page Create Form"
    context['form'] = PageModelForm(instance=item)
    if request.method == 'POST':
        form = PageModelForm(request.POST, request.FILES, instance=item)
        if form.is_valid() :
            item = form.save(commit=False)
            if item.slug == "":
                item.slug = slugify(item.title.replace('ı','i'))
            item.save()
            messages.success(request, 'updated')
            return redirect('page_update', pk)

    return render(request, 'manage/form.html', context)


def page_delete(request, pk) :
    item = Page.objects.get(pk=pk )
    item.status = 'deleted'
    item.save()
    return redirect('page_list')


def page_view(request, page_slug):
    page = get_object_or_404(Page, slug=page_slug)
    context = dict(
        page=page,
    )
    return render(request, "page/page_detail.html", context)


# Admin : 
def carousel_list(request):
    context = dict()
    context['carousel'] = Carousel.objects.all().order_by('-pk');
    return render(request, 'manage/carousel_list.html', context)


def carousel_update(request, pk):
    context = dict()
    item = Carousel.objects.get(pk=pk)
    context['title'] = f"{item.title} - Carousel Create Form"
    context['form'] = CarouselModelForm(instance=item)
    if request.method == 'POST':
        form = CarouselModelForm(request.POST, request.FILES, instance=item)
        if form.is_valid() : 
            form.save()
            messages.success(request, 'updated')
            return redirect('carousel_update', pk)

    return render(request, 'manage/form.html', context)


def carousel_form(request=None, instance=None):
    if request:
        form = CarouselModelForm(
            request.POST,
            request.FILES,
            instance=instance,
        )
    else:
        form = CarouselModelForm(instance=instance)
    return form


def carousel_create(request):
    context = dict()
    context['title'] = "Carousel Create Form"
    context['form'] = CarouselModelForm()

    #item = Carousel.objects.first()
    #context['form'] = CarouselModelForm(instance=item)

    if request.method == 'POST':
        form = CarouselModelForm(request.POST, request.FILES)
        print(form)
        if form.is_valid() :
            form.save()

        messages.success(request, "successfull")
    return render(request, "manage/form.html", context)


