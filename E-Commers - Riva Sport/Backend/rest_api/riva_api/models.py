from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class Seller(models.Model):
    username = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True, to_field='username')
    name = models.CharField(max_length=25, db_index=True, unique=True)
    address = models.TextField(max_length=200, null=True, blank=True)
    email = models.EmailField()
    image = models.ImageField(upload_to="images/profiles/", null=True, blank=True,)
    
    def __str__(self):
        return self.name
    
class Category(models.Model):
    name = models.CharField(max_length=25,unique=True, db_index=True)
    def __str__(self):
        return self.name

class Inventory(models.Model):
    #related_name adl agar bisa dipanggil dari sisi one-nya
    seller = models.ForeignKey(Seller, related_name="inventorys", related_query_name="inventorys" ,on_delete=models.CASCADE, to_field="name", blank=True)
    category = models.ForeignKey(Category, related_name="items", related_query_name="items" ,on_delete=models.CASCADE, to_field="name")
    name = models.CharField(max_length=25, db_index=True)
    slug = models.SlugField(blank=True)
    stock = models.IntegerField()
    price = models.IntegerField()
    description = models.TextField(max_length=300)
    image = models.ImageField(upload_to="images/products/", null=True, blank=True)
    created_at = models.DateField(auto_now=True)

    class Meta:
        ordering = ['slug']

    def __str__(self):
        return f"{self.category} - {self.name}"
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Inventory, self).save(*args, **kwargs)
    


    