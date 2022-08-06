import re
from parsel import Selector
from equity.model.asset_data import AssetData


class Scraper:

    def __init__(self, html: str) -> None:
        self.SELECTOR = Selector(html)

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        del self.SELECTOR

    def __scrapeLabel(self):
        label = self.SELECTOR.css('.zzDege::text').get()
        if not label:
            return ''

        return label

    def __scrapePrice(self):
        price_str = self.SELECTOR.css('div.YMlKec.fxKbKc::text').get()
        if not price_str:
            return 0.00

        # Exclude everything except numbers & '.' (decimal place) to make float compatible.
        price = re.sub(r'([^.0-9])+', '', price_str)

        return float(price)

    def scrapeAssetPage(self):
        label = self.__scrapeLabel()
        price = self.__scrapePrice()

        # TODO: Rest of data...
