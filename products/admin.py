from django.contrib import admin
from .models import Product, Category, Size, ProductSize



class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1  # Number of empty forms to display
    min_num = 1  # Minimum number of forms to display
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [        
        'name',
        'category',      
        'sku',
        'image',
        ] 
    
    inlines = [ProductSizeInline]
    
    ordering = ('name',)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['size_name', 'description']  
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


@admin.register(ProductSize)
class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'price'] 