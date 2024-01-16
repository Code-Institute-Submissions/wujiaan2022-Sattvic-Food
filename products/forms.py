from django import forms
from django.forms import modelformset_factory
from .widgets import CustomClearableFileInput
from .models import Product, Category, Size, ProductSize


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 
        

class ProductSizeForm(forms.ModelForm):    
    
    class Meta:
        model = ProductSize
        # fields = ['size', 'price']
        fields = '__all__'  
        exclude = ['product']       
                

class CustomProductSizeFormSet(modelformset_factory(ProductSize, form=ProductSizeForm, extra=1, can_delete=True)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.forms:
            # Exclude the 'product' field from each form
            form.fields.pop('product', None)       
        
