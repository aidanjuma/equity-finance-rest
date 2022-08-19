import re
from parsel import Selector

from equity.models.asset.asset_model import Asset
from equity.models.asset.asset_data_model import AssetData
from equity.models.asset.asset_type_enum import AssetType
from equity.models.news.news_model import News
from equity.providers.google.market_data import *


class GoogleFinanceScraper:

    def __init__(self, html: str) -> None:
        self.SELECTOR = Selector(html)

    def __enter__(self) -> None:
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        del self.SELECTOR

    def __makeStringFloatCompatible(self, string: str) -> str:
        # Exclude everything except numbers & '.' (decimal place) to make float compatible.
        return re.sub(r'([^.0-9])+', '', string)

    def __formatRangeData(self, data: str) -> dict:
        seperated = data.split('-', maxsplit=2)

        low = self.__makeStringFloatCompatible(seperated[0])
        high = self.__makeStringFloatCompatible(seperated[1])

        return {'low': low, 'high': high}

    def __numberAbbreviationToInteger(self, abbr: str):
        float_compatible = self.__makeStringFloatCompatible(abbr)
        string = re.sub(r'([.0-9])+', '', abbr).replace(' ', '')

        # Filter out currency for market cap, leave just the indicator behind.
        if len(string) > 1:
            for i in each_unique_currency:
                if i in string:
                    string = string.replace(i, '')

        match string:
            case 'K':
                value = int(float(float_compatible) * 1_000)
            case 'M':
                value = int(float(float_compatible) * 1_000_000)
            case 'B':
                value = int(float(float_compatible) * 1_000_000_000)
            case 'T':
                value = int(float(float_compatible) * 1_000_000_000_000)
            case _:
                return 0

        return value

    def __scrapeLabel(self):
        label = self.SELECTOR.css('.zzDege::text').get()
        if not label:
            return ''

        return label

    def __deduceCurrency(self, market: str):
        try:
            currency = market_currencies[market]
            return currency
        except KeyError:
            currency = ''

    def __scrapePrice(self):
        price_str = self.SELECTOR.css('div.YMlKec.fxKbKc::text').get()
        if not price_str:
            return 0.00

        price = self.__makeStringFloatCompatible(price_str)

        return float(price)

    def __scrapeMarketSummary(self):
        path = self.SELECTOR.css('div.PdOqHc::text').get().upper()
        properties = self.SELECTOR.css('span.w2tnNd::text').get().upper()
        table = self.SELECTOR.css(
            'div div.eYanAe div.gyFHrc div.P6K39c::text').getall()

        """ 'Previous Close' is a metric used across all assets
        on Google Finance, and can be obtained in the same way: """
        previous_close = self.__makeStringFloatCompatible(table[0])

        if 'CURRENCY' in path:
            return {'type': AssetType.CURRENCY, 'previous_close': previous_close}

        # Anything below here has a day_range property:
        day_range = self.__formatRangeData(data=table[1])

        # Futures' specific data properties...
        if 'FUTURES' in properties:
            volume = self.__numberAbbreviationToInteger(abbr=table[2])
            primary_exchange = str(table[3])
            market_segment = str(table[4])
            open_interest = self.__numberAbbreviationToInteger(
                abbr=table[5])
            settlement_price = self.__makeStringFloatCompatible(table[6])

            return {
                'previous_close': previous_close,
                'day_range': day_range,
                'volume': volume,
                'primary_exchange': primary_exchange,
                'market_segment': market_segment,
                'open_interest': open_interest,
                'settlement_price': settlement_price
            }

        # Anything below here has a year_range property:
        year_range = self.__formatRangeData(data=table[2])

        if 'INDEX' in path:
            return {'type': AssetType.INDEX, 'previous_close': previous_close, 'day_range': day_range, 'year_range': year_range}

        # Anything below here is a stock; return with scraped data.
        market_cap = self.__numberAbbreviationToInteger(abbr=table[3])
        avg_volume = self.__numberAbbreviationToInteger(abbr=table[4])
        pte_ratio = str(table[5])
        dividend_yield = str(table[6])

        return {
            'previous_close': previous_close,
            'day_range': day_range,
            'year_range': year_range,
            'market_cap': market_cap,
            'avg_volume': avg_volume,
            'p/e_ratio': pte_ratio,
            'dividend_yield': dividend_yield
        }

    def __scrapeAbout(self):
        try:
            about = str(self.SELECTOR.css('div.bLLb2d::text').get())
        except Exception:
            return ''

        return about

    def __scrapeNews(self):
        data = []

        if self.SELECTOR.css('.yY3Lee').get():
            for i, news in enumerate(self.SELECTOR.css('.yY3Lee'), start=1):
                data.append(
                    News(
                        number=i,
                        title=news.css('.Yfwt5::text').get(),
                        link=news.css('.z4rs2b a::attr(href)').get(),
                        source=news.css('.sfyJob::text').get(),
                        published=news.css('.Adak::text').get(),
                        thumbnail=news.css('img.Z4idke::attr(src)').get()
                    )
                )

        return data

    def scrapeAssetPage(self, asset: Asset):
        label = self.__scrapeLabel()
        currency = self.__deduceCurrency(market=asset.market)
        price = self.__scrapePrice()
        market_summary = self.__scrapeMarketSummary()
        about = self.__scrapeAbout()
        news = self.__scrapeNews()

        return AssetData(ticker=asset.ticker,
                         market=asset.market,
                         google_finance_url=asset.google_finance_url,
                         label=label,
                         currency=currency,
                         price=price,
                         market_summary=market_summary,
                         about=about,
                         news=news
                         )

    def scrapeNewsStories(self):
        news = self.__scrapeNews()
        return news
