from abc import ABC, abstractmethod


class BrandScrapingStrategy(ABC):
    # Strategy for scraping a single brand page

    @abstractmethod
    def scrape(self, driver, brand_name, brand_id):
        pass
