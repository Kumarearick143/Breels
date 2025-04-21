from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_cart, name='view_cart'),  # Cart ka main page
    path('add/<int:post_id>/', views.add_to_cart, name='add_to_cart'),  # Add to Cart
    path('remove/<int:post_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove from Cart
]