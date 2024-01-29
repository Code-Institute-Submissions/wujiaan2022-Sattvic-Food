from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    
    path('add_card/<int:product_size_id>/', views.add_to_bag_fromCard, name='add_to_bag_fromCard'),    
    
    path('add/<int:product_size_id>/', views.add_to_bag, name='add_to_bag'),
    
    path('adjust/<product_size_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<product_size_id>/', views.remove_from_bag, name='remove_from_bag'),
]