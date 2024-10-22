from django.conf import settings

from brands.models import Brand
from main.celery import app
from scraping.amazon_brand_scraping import AmazonBrandScrapingStrategy
from scraping.product_services import ScrappingService


@app.task(autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_reties': settings.CELERY_MAX_RETRY})
def run_product_scraping():
    strategy = AmazonBrandScrapingStrategy()
    scrapping_service = ScrappingService(strategy)
    scrapping_service.generate_brand_products(Brand.objects.all())
