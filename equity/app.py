from flask import Flask, request, jsonify
from equity.provider.mongo import MongoProvider
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


if __name__ == '__main__':
    app.run(debug=True)
