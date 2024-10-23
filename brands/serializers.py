from rest_framework import serializers
from rest_framework.reverse import reverse

from brands.models import Product, Brand


class BrandSerializer(serializers.ModelSerializer):
    products_url = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = (
            'name',
            'identifier',
            'products_url',
        )

    def get_products_url(self, obj):
        request = self.context.get('request')
        return reverse('brands:brand_products', kwargs={'brand_id': obj.pk}, request=request)


class ProductSerializer(serializers.ModelSerializer):
    brand = serializers.ReadOnlyField(source='brand.name')

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'asin',
            'sku',
            'image_url',
            'brand',
        )
