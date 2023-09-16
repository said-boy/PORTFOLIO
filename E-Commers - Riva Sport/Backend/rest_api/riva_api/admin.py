from django.contrib import admin
from .models import Category,Inventory,Seller
# Register your models here.

admin.site.register(Category)
admin.site.register(Inventory)
admin.site.register(Seller)