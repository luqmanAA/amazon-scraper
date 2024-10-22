import random
import time

from brands.models import Product, ProductScrapingHistory
from scraper.driver_factory import DriverFactory
from scraper.scraping_strategy import BrandScrapingStrategy


class ScrappingService:
    def __init__(self, scraping_strategy: BrandScrapingStrategy):
        self.scraping_strategy = scraping_strategy

    def generate_brand_products(self, brands):
        """Main function to iterate over brands and scrape products."""
        for brand in brands:
            driver = DriverFactory.create_driver()  # Create a driver via factory
            products = self.scraping_strategy.scrape(driver, brand.name, brand.id)
            self.bulk_create_brand_product(products, brand)
            time.sleep(random.uniform(5, 10))

        brand_names = list(brands.values_list('name', flat=True))
        print(f"Scraping done for {len(brands)} brands: {brand_names}")

    @staticmethod
    def bulk_create_brand_product(products_data, brand):
        """Bulk create or update product information."""
        if products_data:
            products_obj = [Product(**product) for product in products_data]
            Product.objects.bulk_create(
                products_obj,
                update_conflicts=True,
                unique_fields=['brand', 'asin'],
                update_fields=['name', 'sku', 'image_url']
            )

        ProductScrapingHistory.objects.create(
            brand_id=brand.id,
            product_count=len(products_data)
        )

        print(f"{len(products_data)} product(s) scraped for {brand.name}")

