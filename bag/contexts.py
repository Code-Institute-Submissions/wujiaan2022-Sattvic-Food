from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product, Category, Size, ProductSize


def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_id, item_data in bag.items():
        
        product = get_object_or_404(Product, pk=item_id)

        if isinstance(item_data, int):
            # For items without size, default size or single size handling
            product_size = ProductSize.objects.filter(product=product).first()
            
            if product_size:
                total += item_data * product_size.price
                product_count += item_data
                bag_items.append({
                    'item_id': item_id,
                    'quantity': item_data,
                    'product_size': product_size,
                    'product': product,
                })
        else:
            # For items with sizes
            for size_id, quantity in item_data.get('items_by_size', {}).items():
                
                size = get_object_or_404(Size, pk=size_id)
                product_size = get_object_or_404(ProductSize, product=product, size=size)
                
                total += quantity * product_size.price
                product_count += quantity
                
                bag_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product_size': product_size,
                    'product': product,
                    'size': size,
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