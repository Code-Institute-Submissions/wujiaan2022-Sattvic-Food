from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_bag, name='view_bag'),
    
    path('add_to_bag_from_card/<int:item_id>/', views.add_to_bag_fromCard, name='add_to_bag_fromCard'),
    
    path('add/<item_id>/', views.add_to_bag, name='add_to_bag'),
    path('adjust/<item_id>/', views.adjust_bag, name='adjust_bag'),
    path('remove/<item_id>/', views.remove_from_bag, name='remove_from_bag'),
]