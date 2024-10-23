from rest_framework.generics import ListAPIView

from brands.models import Product, Brand
from brands.serializers import ProductSerializer, BrandSerializer


# Create your views here.


class BrandListAPIView(ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()
    search_fields = ['name', ]


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer
    search_fields = ['name', 'asin', ]

    def get_queryset(self):
        params = {}
        if self.kwargs.get('brand_id'):
            params['brand_id'] = self.kwargs.get('brand_id')
        return Product.objects.filter(**params)

