from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class Brand(BaseModel):
    name = models.CharField(max_length=100)
    identifier = models.CharField(max_length=100, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name


class BrandAwareModel(BaseModel):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Product(BrandAwareModel):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=50, unique=True)
    sku = models.CharField(max_length=50, null=True)
    image_url = models.CharField(max_length=255, null=True)

    class Meta:
        ordering = ('-created_at',)
        unique_together = ('brand', 'asin',)

    def __str__(self):
        return self.asin


class ProductScrapingHistory(BrandAwareModel):
    product_count = models.PositiveIntegerField(default=0)
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Scraping history [{self.id}] for {self.brand}"
