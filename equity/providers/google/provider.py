from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

from equity.models.asset.google.asset_model import GoogleAsset
from equity.providers.google.scraper import GoogleFinanceScraper
from equity.providers.google.market_data import iso4217_currencies


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

    def getAssetData(self, asset: GoogleAsset):
        try:
            self.DRIVER.get(asset.google_finance_url)
            self.__rejectGoogleCookies()
            WebDriverWait(self.DRIVER, timeout=3).until(
                EC.presence_of_element_located((By.ID, 'wiz_jd')))
        except TimeoutException:
            raise TimeoutException(
                'Request to Google Finance timed out; please try again.')
        except Exception as err:
            raise Exception(f'An error has occurred: {err}')
        finally:
            scraper = GoogleFinanceScraper(html=self.DRIVER.page_source)
            data = scraper.scrapeAssetPage(asset=asset)

            return data

    def getCurrencyData(self, base: str, quote: str):
        base = base.upper()
        quote = quote.upper()

        if base and quote not in iso4217_currencies:
            raise Exception

        ticker = f'{base}-{quote}'
        asset: GoogleAsset = GoogleAsset(
            ticker=ticker, market='N/A', google_finance_url=f'https://google.com/finance/quote/{ticker}')

        data = self.getAssetData(asset=asset)

        return data

    def getNewsStories(self):
        try:
            self.DRIVER.get('https://www.google.com/finance')
            self.__rejectGoogleCookies()
            WebDriverWait(self.DRIVER, timeout=3).until(
                EC.presence_of_element_located((By.ID, 'wiz_jd')))
        except TimeoutException:
            raise TimeoutException(
                'Request to Google Finance timed out; please try again.')
        except Exception as err:
            raise Exception(f'An error has occurred: {err}')
        finally:
            scraper = GoogleFinanceScraper(html=self.DRIVER.page_source)
            data = scraper.scrapeNewsStories()

            return data
