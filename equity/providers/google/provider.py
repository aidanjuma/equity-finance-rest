from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

from equity.models.asset.asset_model import Asset
from equity.providers.google.scraper import GoogleFinanceScraper


class GoogleFinanceProvider:

    def __init__(self) -> None:
        __driver_options = Options()
        __driver_options.add_argument('--lang=en')
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

    def __rejectGoogleCookies(self) -> None:
        try:
            self.DRIVER.find_element(
                By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button').click()
        except NoSuchElementException:
            return

    def getAssetData(self, asset: Asset):
        try:
            self.DRIVER.get(asset.google_finance_url)
            self.__rejectGoogleCookies()
            # TODO: Adequate wait for element to load/be visible et al.
        except TimeoutError:
            raise TimeoutError(
                'Request to Google Finance timed out; please try again.')
        except Exception as err:
            raise Exception(f'An error has occurred: {err}')
        finally:
            scraper = GoogleFinanceScraper(
                html=self.DRIVER.page_source, asset=asset)
            # TODO: Finish Scraper class and return data as AssetData() object.
            data = scraper.scrapeAssetPage()

            return data
