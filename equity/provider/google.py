import json
from equity.model.asset import Asset
from equity.model.asset_data import AssetData
from parsel import Selector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class GoogleFinanceProvider:

    def __init__(self) -> None:
        __driver_options = Options()
        __driver_options.add_argument('--headless')
        __driver_options.add_argument('--incognito')
        __driver_options.add_argument(
            '--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"')

        self.DRIVER = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=__driver_options)

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.DRIVER.quit()

    def scrapeAssetData(self, asset: Asset):
        try:
            self.DRIVER.get(asset.google_finance_url)
            # TODO: accept cookies, then proceed to scrape data from page.
        except TimeoutError:
            raise TimeoutError(
                'Request to Google Finance timed out; please try again.')
        except Exception as err:
            raise Exception(f'An error has occurred: {err}')
