from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q, Prefetch

from django.db.models.functions import Lower
from django.db.models import Min, F, ExpressionWrapper, DecimalField
from django.db.models import Subquery

from .models import Product, Category, Size, ProductSize
from .forms import ProductForm,  ProductSizeForm, CustomProductSizeFormSet


def all_products(request):
    """ A view to show all products, including sorting and search queries """

    # Fetch all ProductSize instances, sorted by price
    product_sizes = ProductSize.objects.all().order_by('price')

    # Prefetch related products (optional, for performance improvement)
    products = Product.objects.prefetch_related(
        Prefetch('productsize_set', queryset=product_sizes, to_attr='sizes')
    )
      
    query = None
    categories = None
    sort = None
    direction = None

    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
            
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')
            products = products.filter(category__name__in=categories)
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


# def all_products(request):
#     """ A view to show all products, including sorting and search queries """

#     products = Product.objects.all()
    
#    # Calculate and set minimum prices for each product using ProductSize model
#     products = products.annotate(minPriceAnnotation=Min('productsize__price'))
    
#     query = None
#     categories = None
#     sort = None
#     direction = None

#     if request.GET:
#         if 'sort' in request.GET:
#             sortkey = request.GET['sort']
#             sort = sortkey
#             if sortkey == 'name':
#                 sortkey = 'lower_name'
#                 products = products.annotate(lower_name=Lower('name'))
#             if sortkey == 'category':
#                 sortkey = 'category__name'
                
#             if sortkey == 'minPriceAnnotation':
#             # Sort by the annotated 'min_price_annotation' field
#                 sortkey = 'minPriceAnnotation'    
               
#             if 'direction' in request.GET:
#                 direction = request.GET['direction']
#                 if direction == 'desc':
#                     sortkey = f'-{sortkey}'
#             products = products.order_by(sortkey)            
            
#         if 'category' in request.GET:
#             categories = request.GET['category'].split(',')
#             products = products.filter(category__name__in=categories)
#             categories = Category.objects.filter(name__in=categories)

#         if 'q' in request.GET:
#             query = request.GET['q']
#             if not query:
#                 messages.error(request, "You didn't enter any search criteria!")
#                 return redirect(reverse('products'))
            
#             queries = Q(name__icontains=query) | Q(description__icontains=query)
#             products = products.filter(queries)

#     current_sorting = f'{sort}_{direction}'

#     context = {
        
#         'products': products,
#         'search_term': query,
#         'current_categories': categories,
#         'current_sorting': current_sorting,
#     }

#     return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    # Fetch the Product instance using the provided product_id
    product = get_object_or_404(Product, pk=product_id)

    # Fetch related ProductSize instances for this product
    product_sizes = ProductSize.objects.filter(product=product)

    context = {
        'product': product,
        'product_sizes': product_sizes,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        product_size_form = ProductSizeForm(request.POST)

        if product_form.is_valid() and product_size_form.is_valid():
            # Process and save forms individually
            product = product_form.save()
            product_size = product_size_form.save(commit=False)            
            
            product_size.product = product
            product_size.save()
            
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            # Display form validation errors
            messages.error(request, 'Failed to add product. Please correct the form errors.')
    else:
        product_form = ProductForm()
        product_size_form = ProductSizeForm()
        
    template = 'products/add_product.html'
    context = {
        'product_form': product_form,
        'product_size_form': product_size_form,
    }

    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, id=product_id)
    product_sizes = ProductSize.objects.filter(product=product)
    
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        print('Product form instance:')
        # print(product_form)
        
        product_size_formset = CustomProductSizeFormSet(request.POST, queryset=product_sizes)     
        
        if product_form.is_valid() and product_size_formset.is_valid():
            
            product = product_form.save()
            print('product form save success')
            
            for form in product_size_formset:
                if form.cleaned_data.get('DELETE'):
                    if form.instance.id:
                        form.instance.delete()
                else:
                    product_size = form.save(commit=False)
                    product_size.product = product
                    product_size.save()
          
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            print(product_form.errors)
            print(product_size_formset.errors)
            print('POST data:')
            print(request.POST)
            print('Failed to update product. Please ensure the form is valid.')
            
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        product_form = ProductForm(instance=product)
        product_size_formset = CustomProductSizeFormSet(queryset=product_sizes)

        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'product_form': product_form,
        'product_size_formset': product_size_formset,
        'product': product,
    }

    return render(request, template, context)


@login_required
def delete_product_confirm(request, product_id):
    """ Display a confirmation page for deleting a product """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    
    return render(request, 'products/delete_product_confirm.html', {'product': product})


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        # If the user confirms the deletion, delete the product
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))
    
   