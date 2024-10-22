from django.urls import path

from brands.views import ProductListAPIView, BrandListAPIView

app_name = 'brands'

urlpatterns = [
    path('', BrandListAPIView.as_view(), name='brands'),
    path('<int:brand_id>/products', ProductListAPIView.as_view(), name='products'),
]
