from flask import Flask, request, Response
import json
from recommender import initialize_model, recommend_items, get_status, add_product, add_purchase

app = Flask(__name__)

def response_with(data):
    return Response(json.dumps(data), mimetype='application/json')


@app.route('/')
def index():
    return response_with(get_status())


@app.route('/initialize', methods=['GET'], defaults={'force': None})
@app.route('/initialize/<force>', methods=['GET'])
def initialize(force = False):
    return response_with(initialize_model(force))

@app.route('/recommend/<customer>', methods=['GET'])
def recommend(customer=None):
    if customer == None:
        raise Exception("Provide a customer_reference!")
    return response_with(recommend_items(customer))

@app.route('/analyze/<customer>', methods=['GET'])
def analyze(customer=None):
    return "analyzed!"

@app.route('/event/new-product', methods=['POST'])
def new_product():
    new_product = request.get_json()
    return response_with(add_product(new_product))

@app.route('/event/new-purchase', methods=['POST'])
def new_purchase():
    new_purchase = request.get_json()
    return response_with(add_purchase(new_purchase))

if __name__ == '__main__':
    app.run(debug=True, port=5055)  