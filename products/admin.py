from django.contrib import admin
from .models import Product, Category, Size, ProductSize

# Register your models here.


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Number of empty forms to display    
    
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]


class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price']
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Size)
admin.site.register(ProductSize, ProductSizeAdmin)
