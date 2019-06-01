from django.contrib import admin
from .models import ProductCategory, Product
#from authapp.models import ShopUser

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Product)
#admin.site.register(ShopUser)
