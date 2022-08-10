from flask import Flask, request, jsonify
from equity.provider.mongo import MongoProvider
from equity.provider.google import GoogleFinanceProvider
from equity.model.asset import Asset, AssetSchema

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

    # TODO: jsonify and return.

    return {'今から': '元気だよ～！'}


if __name__ == '__main__':
    app.run(debug=True)
