import re
from parsel import Selector
from equity.model.asset import Asset
from equity.model.asset_data import AssetData
from equity.provider.market_currencies import *


class Scraper:

    def __init__(self, html: str, asset: Asset) -> None:
        self.SELECTOR = Selector(html)
        self.ASSET = asset

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        del self.SELECTOR
        del self.ASSET

    def __makeStringFloatCompatible(self, string: str) -> str:
        # Exclude everything except numbers & '.' (decimal place) to make float compatible.
        return re.sub(r'([^.0-9])+', '', string)

    def __formatRangeData(self, data: str) -> dict:
        seperated = data.split('-', maxsplit=2)

        low = self.__makeStringFloatCompatible(seperated[0])
        high = self.__makeStringFloatCompatible(seperated[1])

        return {'low': low, 'high': high}

    def __numberAbbreviationToInteger(self, abbreviation: str):
        float_compatible = self.__makeStringFloatCompatible(abbreviation)
        match re.sub(r'([.0-9])+', '', abbreviation):
            case 'K':
                value = int(float(float_compatible) * 1_000)
            case 'M':
                value = int(float(float_compatible) * 1_000_000)
            case 'B':
                value = int(float(float_compatible) * 1_000_000_000)
            case 'T':
                value = int(float(float_compatible) * 1_000_000_000_000)

        return value

    def __scrapeLabel(self):
        label = self.SELECTOR.css('.zzDege::text').get()
        if not label:
            return ''

        return label

    def __deduceCurrency(self):
        try:
            currency = market_currencies[self.ASSET.market]
            return currency
        except KeyError:
            currency = ""

    def __scrapePrice(self):
        price_str = self.SELECTOR.css('div.YMlKec.fxKbKc::text').get()
        if not price_str:
            return 0.00

        price = self.__makeStringFloatCompatible(price_str)

        return float(price)

    def __scrapeMarketSummary(self):
        table = self.SELECTOR.css(
            'div div.eYanAe div.gyFHrc div.P6K39c::text').getall()

        # TODO: Appropriate to different asset types; i.e. Index
        previous_close = self.__makeStringFloatCompatible(table[0])
        day_range = self.__formatRangeData(data=table[1])
        year_range = self.__formatRangeData(data=table[2])

        return {'previous_close': previous_close, 'day_range': day_range, 'year_range': year_range}

    def scrapeAssetPage(self):
        label = self.__scrapeLabel()
        currency = self.__deduceCurrency()
        price = self.__scrapePrice()

        # TODO: Rest of data...
