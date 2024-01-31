from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
)
from django.contrib import messages

from products.models import Product

from django.http import HttpResponseRedirect

from django.http import JsonResponse

from django.views.decorators.http import require_POST


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def add_to_bag_fromCard(request, product_size_id):
    """Add a quantity of 1 of the specified product size to the shopping bag from the product card"""
    quantity = 1  # Default quantity is set to 1 for quick add
    bag = request.session.get('bag', {})

     # Convert product_size_id to string (or integer if that's your preference)
    product_size_id = str(product_size_id)

    print("Before adding:")
    print(bag)

    if product_size_id in bag:
        bag[product_size_id] += quantity
    else:
        bag[product_size_id] = quantity

    print("After adding:")
    print(bag)

    request.session['bag'] = bag
    request.session.modified = True  # Ensure session is marked as modified


    # Redirect back to the same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Fallback to home if referer not found


def add_to_bag(request):
    """ Add a quantity of the specified product to the shopping bag """

    if request.method == 'POST':
        
        product_size_id = request.POST.get('product_size_id')
        quantity = request.POST.get('quantity', 1)  # Default to 1 if not set
        
        quantity = int(request.POST.get('quantity', 1))
        
        print("Product Size ID:", product_size_id)
        print("Quantity:", quantity)
        
        # quantity = int(request.POST.get('quantity'))      
        redirect_url = request.POST.get('redirect_url')
        
        bag = request.session.get('bag', {})
        print("Before adding:", bag)

        if product_size_id in bag:
            bag[product_size_id] += quantity
        else:
            bag[product_size_id] = quantity

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
