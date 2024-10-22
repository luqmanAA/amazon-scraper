import random
import time

from bs4 import BeautifulSoup
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from scraping.scraping_strategy import BrandScrapingStrategy


class AmazonBrandScrapingStrategy(BrandScrapingStrategy):
    # Concrete strategy for Amazon scraping

    amazon_base_url = 'https://www.amazon.com'

    def get_soup(self, driver):
        return BeautifulSoup(driver.page_source, "lxml")

    def scrape(self, driver, brand_name, brand_id):
        """Scrape paginated pages for the given brand on Amazon."""
        next_page = True
        scraped_products = []
        self.driver = driver

        # Open Amazon and search for the brand
        driver.get(self.amazon_base_url)
        search_bar = self.get_search_bar(driver)
        search_bar.send_keys(f"{brand_name}")
        search_bar.send_keys(Keys.RETURN)

        # Iterate through paginated pages
        while next_page:
            time.sleep(random.uniform(2, 4))
            soup = self.get_soup(driver)
            page_products = self.scrape_brand_page(soup, brand_id)

            if page_products:
                scraped_products.extend(page_products)

            next_page = self.go_to_next_page(driver)

        driver.quit()  # Close the driver after scraping
        return scraped_products

    def get_search_bar(self, driver):
        """Locate the search bar."""
        search_box_ids = ["twotabsearchtextbox", "nav-search-keywords"]
        for search_id in search_box_ids:
            try:
                search_bar = driver.find_element(By.ID, search_id)
                if search_bar:
                    return search_bar
            except NoSuchElementException:
                continue

    def go_to_next_page(self, driver):
        """Check and click the next page button in the pagination."""

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.s-pagination-next")
            if next_button and next_button.is_enabled():
                next_button.click()
                time.sleep(random.uniform(4, 8))
                return True

        except NoSuchElementException:
            pass

        return False

    def scrape_brand_page(self, soup, brand_id):
        """Scrape product information from a single page."""
        products = soup.find_all("div", {"data-component-type": "s-search-result"})
        product_info_list = []

        for product in products:
            product_info = self.parse_product_info(product)
            if product_info.get('asin'):
                product_info.update({'brand_id': brand_id})
                product_info_list.append(product_info)

        return product_info_list

    def parse_product_info(self, product):
        """Parse the product details using BeautifulSoup."""

        asin = product.get('data-asin')
        name_selector = (
                product.find("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-1") or
                product.find("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-2") or
                product.find("h2", class_="a-size-mini a-spacing-none a-color-base s-line-clamp-3")
        )
        name = name_selector.text.strip() if name_selector else None

        image = product.find("img", class_="s-image")['src'] if product.find("img", class_="s-image") else None
        return {
            "asin": asin,
            "name": name,
            "sku": self.extract_sku(product),
            "image_url": image
        }

    def extract_sku(self, product):
        """Extract SKU or similar identifiers directly from the product listing."""
        sku = None

        # Look for elements that might contain SKU or model number
        sku_element = product.find("span", class_="a-size-base a-color-secondary")

        if sku_element and 'model' in sku_element.text.lower():
            sku = sku_element.text.strip()

        # Check if SKU might be mentioned in the product description or features
        feature_list = product.find_all("span", class_="a-size-base a-color-secondary")
        for feature in feature_list:
            if 'sku' in feature.text.lower():
                sku = feature.text.strip()
                break

        return sku

