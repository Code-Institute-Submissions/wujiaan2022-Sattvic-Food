from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from products.models import Product, Category, Size, ProductSize

from django.http import HttpResponseRedirect

from django.http import JsonResponse
from bag.contexts import bag_contents

from django.views.decorators.http import require_POST


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag_fromCard(request, product_size_id):
    """Add a quantity of 1 of the specified product size to the shopping bag from the product card"""
    quantity = 1  # Default quantity is set to 1 for quick add
    bag = request.session.get('bag', {})

    # Fetch the ProductSize instance from the database
    product_size = get_object_or_404(ProductSize, pk=product_size_id)
    # You can access the related Product directly using the related name or attribute on your model
    product = product_size.product
    
     # Convert product_size_id to string (or integer if that's your preference)
    product_size_id = str(product_size_id)

    print("Before adding:")
    print(bag)

    if product_size_id in bag:
        bag[product_size_id] += quantity
        
        # messages.success(request, f'Updated {product_size.size} {product.name} quantity to your bag')
        
    else:
        bag[product_size_id] = quantity
        
        # messages.success(request, f'Added {product_size.size} {product.name} to your bag')

    print("After adding:")
    print(bag)

    request.session['bag'] = bag
    request.session.modified = True  # Ensure session is marked as modified

    # After updating the bag, get the updated bag context
    context = bag_contents(request)
    grand_total = context['grand_total']
    updated_quantity = bag[str(product_size_id)]
    
    # Return the updated context as part of the JsonResponse
    return JsonResponse({
        'success': True,
        'message': 'Product added to bag!',
        'bag_items_count': context['product_count'],
        'bag_total': float(context['total']),
        'delivery': float(context['delivery']),
        'grand_total': float(context['grand_total']),
        'updated_quantity': updated_quantity
    })


def add_to_bag(request):
    """ Add a quantity of the specified product to the shopping bag """

    if request.method == 'POST': 
             
        product_size_id = request.POST.get('product_size_id')
        # quantity = request.POST.get('quantity', 1)  # Default to 1 if not set
        
        quantity = int(request.POST.get('quantity', 1))
        
        print("Product Size ID:", product_size_id)
        print("Quantity:", quantity)        
          
        redirect_url = request.POST.get('redirect_url')
        
        product_size = get_object_or_404(ProductSize, pk=product_size_id)
        product = product_size.product 
        print(product_size.size, product.name)
        
        bag = request.session.get('bag', {})
        print("Before adding:", bag)

        if product_size_id in bag:
            bag[product_size_id] += quantity
            
            messages.success(request, f'Updated {product_size.size} {product.name} quantity to your bag')
            
        else:
            bag[product_size_id] = quantity
            
            messages.success(request, f'Added {product_size.size} {product.name} to your bag')

        request.session['bag'] = bag  # Save the updated bag back to the session

        print("After adding:", bag)
        
        return redirect(redirect_url)


def adjust_bag(request, product_size_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    
    bag = request.session.get('bag', {})

    if product_size_id in bag:
        if quantity > 0:
            bag[product_size_id] = quantity
        else:
            bag.pop(product_size_id)  

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, product_size_id):
    """Remove the item from the shopping bag"""
    try:
        bag = request.session.get('bag', {})
        
        if product_size_id in bag:
            bag.pop(product_size_id)
            request.session['bag'] = bag

        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)
