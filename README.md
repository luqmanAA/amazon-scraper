# Scraping Service Documentation

This document explains how to set up and use the scraping service for scraping product information from Amazon based on a list of brands.
The service is built using Selenium for web scraping, BeautifulSoup for parsing, and the Django ORM for handling product data storage.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Task](#running the task)

---

## Prerequisites

Before setting up the scraping service, ensure that the following prerequisites are met:

1. **Python >=3.10** should work but this app uses **Python 3.11**.
2. **Django >=4.2.15** should work but the app uses **Django 5.1.1**.
3. **Google Chrome** installed on your system, as the scraper uses the Chrome WebDriver.
4. **Chromedriver** for Selenium (this is handled by `webdriver-manager`).

---

## Installation

1. **Clone this repository**
2. **Start your redis instance. Follow this [guide](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/) to set it up if you don't have one** 
3. Set the environment variables following the sample provided in [`.env.sample`](https://github.com/luqmanAA/amazon-scraper/blob/main/.env.sample).

Set the value of `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` in your .env file to be the redis instance you set up in `2.` above.

4. Set up your virtual environment and install the dependencies by running this command in the project root directory:

```bash
   pip install -r requirements.txt
```
5. **Run migrations**
    ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. **Run this command and follow the prompts to create admin user**
  ```bash
     python manage.py createsuperuser
   ```
7. **Launch the app with the command below**
  ```bash
       python manage.py runserver 3100
   ```
8. **Visit Django admin to create brands and manage other data**

Using your preferred browser, visit: `http:localhost:3100/admin`. Login with the `username` and `password` of the user 
created at 3. above. Click on `Brands` from the left panel, click `ADD BRAND`
button in the top-right corner of the table.


## Running the Task
#### For the steps below to work, it's import that your redis instance (setup in [Installation](#installation) step 2 above) is working perfectly
1. **Start your celery worker and celery beat by running the commands below in separate terminals while being in the project root directory**

```bash
    celery -A main worker -l info -P eventlet
```
```bash
    celery -A main beat -l info
```

### If all steps above are well followed, the app server, celery worker and celery beat should be working, and the task should be ready to fire every 6 hours. Good luck!


## Task Scheduling
The task scheduling was implemented using celery and celery beat.

1. **brands/tasks.py** contains the function (`run_product_scraping()`) to trigger the scrapping.
The `@app.task` decorator on the function contains a retry mechanism.  
```bash
  autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={'max_reties': settings.CELERY_MAX_RETRY} 
```
The `autoretry_for` argument specifies the exception types to retry, `retry_backoff` enables exponential backoff, and `retry_kwargs` sets the maximum number of retries.

2. **main/settings.py** has a `CELERY_BEAT_SCHEDULE` settings that specify the task (i.e task in 1 above) to run and the interval (`every 6 hours`) to run the task


## Scrapping Mechanism
The scrapping mechanism implementation is in the `scraper` directory and contains 4 files handling different part of the scraping, see the explanation below:
1. **driver_factory.py**: This file contains the `DriverFactory` class, which is responsible for creating and configuring the WebDriver instances.
2. **scraping_strategy.py**: This file contains the abstract class `BrandScrapingStrategy` which form a base for all concrete implementation that we might want to create eventually. 
3. **amazon_brand_strategy**: This file contains the `AmazonBrandScrapingStrategy`, a concrete implementation of the `BrandScrapingStrategy` interface designed for scraping product listings on Amazon. 
It handles searching for a specific brand, scraping product details from multiple pages, and navigating through Amazon’s paginated results. 
This class is designed to work with Selenium for driving the browser and BeautifulSoup for parsing the HTML content.

#### The class workflow
* **Search the Brand**: The scrape method searches for a brand on Amazon and retrieves product listings.
* **Paginated Scraping**: It scrapes product data across multiple pages and handles pagination with go_to_next_page.
* **Product Data Extraction**: Product details such as ASIN, name, SKU, and image URL are parsed for each product using parse_product_info and extract_sku.
* **Return Results**: The scraped product information is collected into a list and returned at the end of the process.

5. **product_service.py**: contains the `ScrappingService` class which is responsible for the process of scraping product information for a list of brands using a specified scraping strategy (such as `AmazonBrandScrapingStrategy` from above or any other strategy later). 
It integrates the scraping process, stores scraped data in the database, and keeps track of the scraping history.

#### The class workflow
* **Scraping Initialization**: The service starts by iterating over the list of brands and scraping products using the provided strategy.
* **Selenium Driver**: For each brand, it creates a new Selenium driver to handle browsing and scraping.
* **Scraping Execution**: The scraping strategy's `scrape()` method is called, which takes control of the driver to perform the scraping and returns a list of product data.
* **Product Data Storage**: The `bulk_create_brand_product` method is called to store the scraped product information in the database in an efficient way, using a single query for all product scrapped for a particular brand. This is to limit the database hit to only number of brands. It handles both creating new products and updating existing ones. 
* **Logging Scraping History**: After each brand's products are scraped, a record of the scraping event is stored in the ProductScrapingHistory model with details like brand, number of product scraped and time it was scraped.
* **Pausing Between Brands**: A random delay is introduced between brand scrapes to avoid triggering anti-bot mechanisms on the website being scraped.

## Anti-Scraping Measures
1. This app chose to use Selenium driver for scraping as it provides a way to mimic real user with its various option, such as:
* human-like navigation: Going through the website in a human-like manner, such as making use of the search bar and next button, as against slapping the direct page url on the requests library. 
This is one of the measure put used to bypass Amazon's anti-scraping measure

2. This app uses the `ChromeDriverManager().install()` to correctly install chrome drivers.
3. `Element not found` error on css selector search was handled to fail silently and this is a possible cause for when getting zero product scraped
4. Random delays were added between requests (time.sleep()) to mimic human-like interaction. 
5. User agents were randomly rotated using the fake-useragent library. 
