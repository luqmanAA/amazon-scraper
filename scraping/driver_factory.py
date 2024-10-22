from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverFactory:
    # Factory to create and configure WebDriver instances

    proxy_list = [
        "http://45.119.133.218:3128",
        "http://160.86.242.23:8080",
        "http://20.111.54.16:8123",
        "http://20.111.54.16:8123",
    ]
    user_agent = UserAgent()

    @classmethod
    def create_driver(cls):
        """Creates and configures a Selenium WebDriver."""

        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent={cls.user_agent.random}')
        # Add more options or proxy settings here if needed

        driver_path = ChromeDriverManager().install()
        service = Service(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
