from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Category, Size, ProductSize


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for product_size_id, quantity in bag.items():
        # Retrieve the ProductSize instance
        product_size = get_object_or_404(ProductSize, pk=product_size_id)
        product = product_size.product  # Get the associated Product

        total += quantity * product_size.price
        product_count += quantity

        bag_items.append({
            'product_size_id': product_size_id,
            'quantity': quantity,
            'product_size': product_size,
            'product': product,
        })

    # Calculate delivery costs and grand total
    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context