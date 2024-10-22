from rest_framework.generics import ListAPIView

from brands.models import Product, Brand
from brands.serializers import ProductSerializer, BrandSerializer


# Create your views here.


class BrandListAPIView(ListAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class ProductListAPIView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(
            brand_id=self.kwargs.get('brand_id')
        )

