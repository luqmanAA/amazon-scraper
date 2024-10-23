from django.urls import path

from brands.views import ProductListAPIView, BrandListAPIView

app_name = 'brands'

urlpatterns = [
    path('brands', BrandListAPIView.as_view(), name='brands'),
    path('brands/<int:brand_id>/products', ProductListAPIView.as_view(), name='brand_products'),
    path('products', ProductListAPIView.as_view(), name='products'),
]
