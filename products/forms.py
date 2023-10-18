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
        
        # def clean(self):
        #     cleaned_data = super().clean()
        #     size = cleaned_data.get('size')
        #     price = cleaned_data.get('price')

        #     # Check if the form is marked for deletion
        #     if self.cleaned_data.get('DELETE'):
        #         return cleaned_data  # Skip further validation for deleted forms

        #     # Add your validation logic here for non-deleted forms
        #     if not size:
        #         raise forms.ValidationError("Size is required.")
        #     if price is None:
        #         raise forms.ValidationError("Price is required.")
        #     return cleaned_data
        

class CustomProductSizeFormSet(modelformset_factory(ProductSize, form=ProductSizeForm, extra=1, can_delete=True)):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for form in self.forms:
            # Exclude the 'product' field from each form
            form.fields.pop('product', None)
       
        
# class ProductForm(forms.ModelForm):

#     class Meta:
#         model = ProductSize
#         fields = '__all__'

#     image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         categories = Category.objects.all()
#         friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

#         self.fields['category'].choices = friendly_names
#         for field_name, field in self.fields.items():
#             field.widget.attrs['class'] = 'border-black rounded-0'