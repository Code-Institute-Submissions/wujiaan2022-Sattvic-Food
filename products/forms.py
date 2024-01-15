from django import forms
from .widgets import CustomClearableFileInput

from .models import Category, Size, Product, ProductSize

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'friendly_name']

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size_name', 'description']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'sku', 'name', 'description', 'rating', 'image_url', 'image']

class ProductSizeForm(forms.ModelForm):
    class Meta:
        model = ProductSize
        fields = ['product', 'size', 'price']