from django.db import models
from django.db.models import Min


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'
        
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Size(models.Model):
    size_name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.size_name
    

class ProductSize(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    size = models.ForeignKey('Size', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        unique_together = ('product', 'size')

    def __str__(self):
        return f"{self.product.name} - {self.size.size_name}"


class Product(models.Model):
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    
    min_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    
    description = models.TextField()  
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True) 
    
    def __str__(self):
        return self.name
    
    # Define a method to calculate and set the minimum price
    def calculate_min_price(self):
        min_price = self.productsize_set.aggregate(min_price=Min('price'))['min_price']
        self.min_price = min_price
        self.save()