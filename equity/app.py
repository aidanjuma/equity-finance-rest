from flask import Flask, request, jsonify
from equity.models.asset.asset_data_model import AssetDataSchema
from equity.models.asset.asset_model import *
from equity.models.news.news_model import *
from equity.providers.mongo.provider import MongoProvider
from equity.providers.google.provider import GoogleFinanceProvider

app = Flask(__name__)


@app.route('/google/assets', methods=['GET'])
def google_assets():
    limit = int(request.args['limit'])
    offset = int(request.args['offset'])

    with MongoProvider() as mongo:
        assets: list(Asset) = mongo.getGoogleAssets(limit=limit, offset=offset)

    prev_url = f'/google/assets?limit={limit}&offset={offset - limit}'
    next_url = f'/google/assets?limit={limit}&offset={offset + limit}'

    schema = AssetSchema(many=True)

    return jsonify({'result': schema.dump(assets), 'prev_url': prev_url, 'next_url': next_url})


@app.route('/google/data/<ticker>', methods=['GET'])
def google_assets_data(ticker: str):
    market = None
    if request.args:
        market = str(request.args['market'])

    with MongoProvider() as mongo:
        assets: list(Asset) = mongo.getGoogleAssetsToScrape(ticker, market)

    data = []
    with GoogleFinanceProvider() as google:
        for asset in assets:
            data.append(google.getAssetData(asset))

    schema = AssetDataSchema(many=True)

    return jsonify({'result': schema.dump(data)})


# Get news top stories; TODO -> Local, World Markets?
@app.route('/google/news', methods=['GET'])
def google_news():
    with GoogleFinanceProvider() as google:
        news: list(News) = google.getNewsStories()

    schema = NewsSchema(many=True)

    return jsonify({'result': schema.dump(news)})


if __name__ == '__main__':
    app.run(debug=True)
