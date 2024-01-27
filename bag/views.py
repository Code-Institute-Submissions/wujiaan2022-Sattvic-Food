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


def add_to_bag_fromCard(request, item_id):
    """ Add a quantity of 1 of the specified product to the shopping bag from the product card """

    quantity = 1  # Default quantity is set to 1 for quick add
    size = None
    if 'product_size' in request.GET:  # Assuming size is passed as a GET parameter
        size = request.GET['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity

    request.session['bag'] = bag

    # Redirect back to the same page
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Fallback to home if referer not found


# def add_to_bag_fromCard(request, item_id):
#     """ Add a quantity of 1 of the specified product to the shopping bag from the product card """

#     size = None
#     if 'product_size' in request.GET:
#         size = request.GET['product_size']
    
#     # Create a unique key for the product and size combination
#     item_key = f"{item_id}_{size}" if size else str(item_id)
    
#     bag = request.session.get('bag', {})

#     # Check if the unique item_key is already in the bag
#     if item_key in bag:
#         # Increment quantity for existing item
#         bag[item_key]['quantity'] += 1
#     else:
#         # Add new item to the bag with quantity set to 1
#         bag[item_key] = {'quantity': 1, 'size': size} if size else {'quantity': 1}

#     request.session['bag'] = bag

#     # Redirect back to the same page
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))  # Fallback to home if referer not found



def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))      
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
            else:
                bag[item_id]['items_by_size'][size] = quantity
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
    # else:
    #     if item_id in list(bag.keys()):
    #         bag[item_id] += quantity
    #     else:
    #         bag[item_id] = quantity

    request.session['bag'] = bag
    
    print(request.session['bag'])
    
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
    else:
        if quantity > 0:
            bag[item_id] = quantity
        else:
            bag.pop(item_id)

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""

    try:
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
        else:
            bag.pop(item_id)

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        return HttpResponse(status=500)

