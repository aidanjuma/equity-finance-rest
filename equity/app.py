from flask import Flask, request, jsonify

from equity.models.asset.google.asset_data_model import GoogleAssetDataSchema
from equity.models.asset.binance.asset_data_model import *
from equity.models.asset.google.asset_model import *
from equity.models.news.google.news_model import *
from equity.models.asset.binance.asset_model import *
from equity.providers.mongo.provider import MongoProvider
from equity.providers.google.provider import GoogleFinanceProvider
from equity.providers.binance.provider import BinanceProvider

app = Flask(__name__)


@app.route('/google/assets', methods=['GET'])
def google_assets():
    limit = int(request.args['limit'])
    offset = int(request.args['offset'])
    with MongoProvider() as mongo:
        assets: list(GoogleAsset) = mongo.getGoogleAssets(
            limit=limit, offset=offset)

    prev_url = f'/google/assets?limit={limit}&offset={offset - limit}'
    next_url = f'/google/assets?limit={limit}&offset={offset + limit}'

    schema = GoogleAssetSchema(many=True)

    return jsonify({'result': schema.dump(assets), 'prev_url': prev_url, 'next_url': next_url})


@app.route('/google/data/<ticker>', methods=['GET'])
def google_assets_data(ticker: str):
    ticker = ticker.upper()
    market = None
    if request.args:
        market = str(request.args['market'])

    with MongoProvider() as mongo:
        assets: list(GoogleAsset) = mongo.getGoogleAssetsToScrape(
            ticker, market)

    data = []
    with GoogleFinanceProvider() as google:
        for asset in assets:
            data.append(google.getAssetData(asset))

    schema = GoogleAssetDataSchema(many=True)

    return jsonify({'result': schema.dump(data)})


@app.route('/google/data/currency', methods=['GET'])
def google_currency():
    base = request.args['base']
    quote = request.args['quote']
    with GoogleFinanceProvider() as google:
        try:
            asset = google.getCurrencyData(base=base, quote=quote)
        except Exception:
            return jsonify({'error_code': 404, 'message': 'One or more of currencies provided was invalid; please try different value(s).'})

    schema = GoogleAssetDataSchema()

    return jsonify({'result': schema.dump(asset)})


@app.route('/google/news', methods=['GET'])
def google_news():
    with GoogleFinanceProvider() as google:
        news: list(GoogleMarketNews) = google.getNewsStories()

    schema = GoogleMarketNewsSchema(many=True)

    return jsonify({'result': schema.dump(news)})


@app.route('/binance/assets', methods=['GET'])
def binance_assets():
    limit = int(request.args['limit'])
    offset = int(request.args['offset'])
    with BinanceProvider() as binance:
        assets: list(BinanceAsset) = binance.getAvailableAssets(
            limit=limit, offset=offset)

    prev_url = f'/binance/assets?limit={limit}&offset={offset - limit}'
    next_url = f'/google/assets?limit={limit}&offset={offset + limit}'

    schema = BinanceAssetSchema(many=True)

    return jsonify({'result': schema.dump(assets), 'prev_url': prev_url, 'next_url': next_url})


@app.route('/binance/data/<ticker>', methods=['GET'])
def binance_assets_data(ticker: str):
    with BinanceProvider() as binance:
        asset: BinanceAssetData = binance.getAssetData(ticker=ticker)

    schema = BinanceAssetDataSchema()

    return jsonify({'result': schema.dump(asset)})


if __name__ == '__main__':
    app.run(debug=True)
