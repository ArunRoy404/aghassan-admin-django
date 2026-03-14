from django.urls import path
from . import views

urlpatterns = [
    # API endpoints
    path('api/products/', views.ProductListAPI.as_view(), name='api_product_list'),
    path('api/products/<int:pk>/', views.ProductDetailAPI.as_view(), name='api_product_detail'),
    path('api/products/<int:pk>/mockup/', views.GenerateMockupAPI.as_view(), name='api_generate_mockup'),

    # Web endpoints
    path('upload/', views.upload_product, name='upload_product'),
    path('list/', views.product_list, name='product_list'),
    path('delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('delete-multiple/', views.delete_multiple_products, name='delete_multiple_products'),
]
