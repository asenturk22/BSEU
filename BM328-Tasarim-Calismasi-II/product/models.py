from django.db import models
from autoslug import AutoSlugField
from django.contrib.auth.models import User


# Third Party Apps:
from django.urls import reverse
from page.models import DEFAULT_STATUS, STATUS


GENDER_CHOICE = [
    ('men', 'Erkek'),
    ('women', 'Kadin'),
    ('unisex', 'UniSex'), 
]


class BaseModel(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True



# Category
class Category(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    )
    gender = models.CharField(
        max_length=6,
        default="unisex",
        choices=GENDER_CHOICE,
    )
    slug = models.SlugField(
        max_length=200,
        default="",
    )
    
    def __str__(self): 
        return f"{self.pk} - {self.gender} - {self.title}"


    def get_absolute_url(self):
        return reverse(
            'page:page_view',
            kwargs={
                'page_slug':self.slug,
            }
        )
    

# Product / Item
class Product(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    product_code = models.CharField(max_length=50) #ürün kodu
    price = models.FloatField()   #birim fiyat
    discount_price = models.FloatField(blank=True, null=True) #indirim
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE
    )
    brand = models.CharField(max_length=50) #Marka
    content = models.TextField()
    cover_image = models.ImageField(
        upload_to='product',
        null=True,
        blank=True,
    )
    slug = models.SlugField(
        max_length=200,
        default="",
    )
    stock = models.PositiveSmallIntegerField(default=0)
    is_home = models.BooleanField(default=False)
    status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    )
    
    def __str__(self): 
        return self.title

    def get_discount_percent(self):
        discount_percent = 100 - (self.discount_price * 100 / self.price)
        return discount_percent

    def get_item_url(self):      
        return reverse('product:detail', kwargs={
            'slug' : self.slug
        })
    
    
    def get_add_to_cart(self):
        return reverse('product:add_to_cart', kwargs={
            'slug' : self.slug
        })
    

    def snip_description(self):
        return self.content[:30] + "..."
    

#OrderItem
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False) #status
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def  __str__(self) :
        return f"{self.quantity} - {self.item.title}"
    
    def total_item_price(self):
        return self.quantity * self.item.price
    
    def total_item_discount_price(self):
        return self.quantity * self.item.discount_price
    
    def amount_saved(self): 
        return self.total_item_price() - self.total_item_discount_price()
    
    def final_price(self):
        if self.item.discount_price:
            return self.total_item_discount_price()
        return self.total_item_price()


#Country
class Countries(models.Model):
    country = models.CharField(max_length=50)

    def  __str__(self) :
        return self.country

#cities
class Cities(models.Model):
    country_id = models.ForeignKey(Countries, on_delete=models.CASCADE)
    city = models.CharField(max_length=50)

    def  __str__(self) :
        return self.city
    
#Towns
class Towns(models.Model):
    city_id = models.ForeignKey(Cities, on_delete=models.CASCADE)
    town = models.CharField(max_length=50)

    def  __str__(self) :
        return self.town

#Districts
class Districts(models.Model):
    town_id = models.ForeignKey(Towns, on_delete=models.CASCADE)
    district = models.CharField(max_length=50)

    def  __str__(self) :
        return self.district

#Address
class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE)
    city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    town = models.ForeignKey(Towns, on_delete=models.CASCADE)
    district = models.ForeignKey(Districts, on_delete=models.CASCADE)
    postal_code = models.CharField(max_length=10)
    address_text = models.CharField(max_length=500)


#Coupon
class Coupon(models.Model):
    code = models.CharField(max_length=20)
    amount = models.FloatField()
    
    def __str__(self):
        return self.code


#Payments
class Payments(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    #payment_type = models.SmallIntegerField(blank=True, null=True)
    #isok = models.BooleanField()
    #approve_code = models.CharField(max_length=100)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    

#Order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_ref = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem) 
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False) #status
    billing_address = models.ForeignKey(
        BillingAddress, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    coupon = models.ForeignKey(
        Coupon, 
        on_delete=models.SET_NULL, 
        blank=True, 
        null=True
    )
    payment = models.ForeignKey(
        Payments,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def  __str__(self) :
        return self.user.username

    def total_price(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.final_price()

        if self.coupon:
            total -=  self.coupon.amount
        return total
  
  

#Refund
class Refund(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"

    


