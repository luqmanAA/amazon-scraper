from django.contrib import admin

from brands.models import Brand, Product, ProductScrapingHistory


# Register your models here.


class BrandAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'identifier',
    )


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'asin',
        'brand',
        'sku',
    )


class ProductScrapingHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'brand',
        'product_count',
        'scraped_at',
    )


admin.site.register(Brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductScrapingHistory, ProductScrapingHistoryAdmin)
