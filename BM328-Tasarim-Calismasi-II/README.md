# DjangoE-Trade App 

> https://djangoogreniyorum.github.io/

1. VirtualEnv kurulumu yapılıyor.  detaylar için  [Virtualenv](https://virtualenvwrapper.readthedocs.io/en/latest/)

## Kurulum

### Python kurulumu

Django freamework'u python ile 
> http://www.python.org

### Virtualenv ortamının kurulumu 

Django kurulmadan önce sanal bir ortam oluşturup onun içine django kurulumunu yapacağız.  Böylelikle her proje kendinden bağımsız kurulumların ve dosyaların olduğu yapıyı oluşturmuş olacağız. Örneğin A projesinde kurulması gereken bir paket B projesinde ihtayaç olmayabilir. Bunun için her proje bir sanal ortam içerisinde olsa ve django kurulumu yapıldıktan sonra her projenin kendi ihtiyacı olan paket kurulumları kendi ortamlarinda olmasi daha güvenli olacaktır.  Bunun için virtualenv sanal ortamindan faydalanacağiz. 

```sh
# Sanal ortam kurulumu yapılıyor. 
pip install virtualenv 

# virtualevn kurulu olup olmadığını kontrol etmek için 
python3 -m virtualenv
```

Virtualenv sanal ortamı kurulduktan sonra projemiz olan DjangoE-Trade_venv  adında sanal ortam kurulumu yapiliyor. 

```sh 
# Sanal ortam kuruluyor.
python3 -m virtualenv DjangoE-Trade_venv

# Sanal ortama giriş yapmak için 
source DjangoE-Trade_venv/bin/activate

# Sanal ortamı sonlandırmak için
deactivate

# Sanal ortamda yüklü paketleri görüntülemek için 
pip freeze
```

Sanal ortam kurulumunu yaptıktan sonra terminal ekranından giriş komutu ile venv sanal ortamına giriş yapıyoruz. 

> https://virtualenvwrapper.readthedocs.io/en/latest/install.html


### Pip kurulumu 

```sh
    pip install --upgrade pip
```

### Django kurulumu

virtualenv sanal ortamının kurulumu yapıldıktan sonra sanal ortam içinde iken pip freeze ile mevcut paketlerin kontrolünü yaptığımızda herhangi bir paket olmadığından ekrana birşey gelmeyecektir.  Bu aşamada ilk önce Python3 ve üzeri sürüm gerekmektedir.  

```sh
    # macOs/linux için 
    python -m pip install Django

    # windows için 
    py -m pip install Django

    pip install --upgrade pip
```

> https://docs.djangoproject.com/en/4.2/topics/install/#installing-official-release


### DjangoE-Trade App Start

Django kurulumu yaptıktan sonra projemizin ilk başlangıç ayarlarını yapalım. 

```sh
django-admin 
```

yazdıktan sonra django ile kurulum yapılacak liste gelecektir. Gelen listede startproject komutu ile projemizi config şeklinde başlatalım. 

```sh
python manage.py startproject config .
```

### App oluşturmak 

// Page App oluşturmak
// Product App
// Cart App

```sh
python manage.py startapp page
python manage.py startapp product
python manage.py cart
```

Oluşturmuş olduğumuz bu Page, Product ve Cart applicaton' ları Config içindeki settings.py dosyası içinde INSTALLED_APPS dizisi içinde tanımlamasını yapıyoruz. 


### Database yapılırının oluşturulması

```sh
python manage.py makemigrations
python manage.py migrate
```

database yapılıarını makemigrations komutu ile model yapısının oluşturulmasını hazırlayıp migrate komutu ile bu yapıya göre databse tablolarının oluşturulmasını sağlar. 

### Template klasörünün oluşturulması 

Djangoda herşey template ler üzerinden gittiğinden ana klasörün altında 
template klasörü oluşturuyoruz.  Ardındn bu klasörü settings.py klasörü içerisinde TEMPLATES dizi içerisindeki key, value değeri içindeki DIRS key'ine tanıtıyoruz. Böylece django templates klasörünün yerini bilip ona göre ilgili işlemlemlerini yapacaktır. 


templates klasörün altında aşağıdaki klasörleri ve dosyaları oluşturuyoruz. 
- base
    - components
        - footer_scripts.html
        - footer.html
        - nav.html
        - head.html
    base.html
- home
    - carousel.html
- page
- product
    - product.html

### static klasörünün oluşturulması

ana klasörümüzün altında static klasörü oluşturuyoruz ve içinde css, js, img klasörleri oluşturup ilgili dosyaları oluşturuyoruz. 

- img
- css
- jss

### page app ayarlarının yapılması 

page/view.py dosyası içerisinde görüntülenecek sayfaların yapısını oluşturuyoruz. 

def home(request): 
    context = dict(
    )
    return render(request, "page/index.html", context)

### page models.py dosyasında tabloların oluşturulması 

- image dosyalarının organizasyonu için pillow kütüphanesinin inidirilmesi
- autoslug kütüphanesinin indirilmesi 
- tinymce kurulumu yapıyoruz. 
- models.py deki modeli makemigrations ardından migrate yap. 
- createsuperuser ile admin kullanıcısı ekliyoruz. 
- model oluşturulduktan sonra bu modeli admin panalinde yönetebilmemiz için page/admin.py dosyasında ilgili işlemleri yap. 
- 

Django 
    - M - DB yapısı
    - V - View / Control
    - T - Template
    - A - Admin
    - F - Forms
    - # - Message
    - # - Session

- Carousel models işlemlerini yap.   page/models.py içinde



TODO :  Yönetici Tarafı
    - carousel girebilmeli
    - page
    - product
    - category 
    - order

TODO : Kullanıcı Tarafı
    - Kullanıcı Kaydı
    - Adres Kaydı
    - Kredi Kartı İşlemleri  / iyzico  -> SUCCESS / ERROR  -> (price değerine bakmak gerekir. )
    - Sipariş Takibi 
    - Cart -> items


*** Yeni Carousel eklemek için;
from page.models import Carousel
Carousel.objects.create(title="new title")

şekline yeni bir elemen eklemiş oluruz. 

- Django form-> Normal form veya model form olmak üzere 2 tür form yapısı vardır. 
page/forms.py  adlı dosyayı oluşturup içine gerekli kodları yazalım. 


Djangoda yorum satırları 
{#  tek satır yorum #}
{% comment %}
    birden
    fazla
    satır 
    yorum
{% endcomment %}


- django-extensions
    x bilgisayarında çalışmasını istediğim şeyleri 
    y bilgisayarında çalışmasını istemeyebilirim. bunlar için
    paketler kurulumunu yapalım. 
    
    pip install ipython 
    pip install django-extensions
    

export DJANGO_DEBUG="True"
