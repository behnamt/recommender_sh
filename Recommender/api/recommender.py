import turicreate as tc
import pandas as ps
import json
from jsonschema import validate, ValidationError

# local imports
from data_service import load_raw_data, save_products, save_transactions
from schema import purchase_schema, product_schema
# CONSTANTS
MODEL_SAVE_PATH = "model/recommendations.model"


# Model
model = None
USER_ID_KEY = 'CUSTOMER'
ITEM_ID_KEY = 'SKU'
TARGET_KEY='COUNT_FREQ'
K = 5

# Data
transactions_raw = None
products_raw = None

# Rest
initialized = False

def load_model():
    global model
    if (not model == None):
        raise Exception("Cannot overwrite the model")
    model = tc.load_model(MODEL_SAVE_PATH)

def save_model():
    global model
    if (model == None):
        raise Exception("Model not found")
    model.save(MODEL_SAVE_PATH)

def add_product(data):
    try:
        global products_raw
        validate(instance=data, schema=product_schema)
        df = ps.json_normalize(data)
        products_raw = products_raw.append(df)
        save_products(products_raw)
        return { 'sucess': True }
    except ValidationError:
        return { 'success': False, 'error': 'the product is not in the correct format' }

def add_purchase(data):
    global transactions_raw, initialized, model
    try:
        validate(instance=data, schema=purchase_schema)
        df = ps.json_normalize(data)
        transactions_raw = transactions_raw.append(df)
        save_transactions(transactions_raw)
        if (initialized):
            model.recommend(new_observation_data=tc.SFrame(df))      
        return { 'sucess': True }
    except ValidationError:
        return { 'success': False, 'error': 'the product is not in the correct format' }

    # model.recommend(new_observation_data=data)

def load_data():
    global transactions_raw, products_raw
    transactions_raw, products_raw = load_raw_data()
    print('Loaded data succesfully')


def get_normilized_data():
    transactions_count = transactions_raw.groupby(['SKU', 'CUSTOMER']).size().reset_index(name='COUNT')
    transactions_count = transactions_count.join(transactions_count.groupby(['SKU'])['COUNT'].transform(lambda x: x / x.sum()), rsuffix='_FREQ')
    print('Normalized the transaction counts')
    return tc.SFrame(transactions_count)

def set_model(data):
    global model
    if (model == None):
        try:
            model = tc.load_model(MODEL_SAVE_PATH)
            print('Loaded model from storage')
        except OSError:
            model = tc.item_similarity_recommender.create(
                data,
                user_id=USER_ID_KEY,
                item_id=ITEM_ID_KEY,
                target=TARGET_KEY,
                similarity_type='cosine')
            model.save(MODEL_SAVE_PATH)
            print('Created new model')

def merge_with_product_info(items):
    products_rec = products_raw[products_raw['SKU'].isin(items['SKU'])] 
    products_rec['COLOR'] = products_rec['ATTRIBUTES'].apply(lambda x: json.loads(x)['color'])
    products_rec['BRAND'] = products_rec['ATTRIBUTES'].apply(lambda x: json.loads(x)['brand'].upper())
    products_rec = ps.merge(items, products_rec, how='left', on=['SKU']).drop_duplicates(subset=['SKU'])
    return products_rec[['rank','score','NAME','BRAND', 'COLOR']].to_json(orient="records")
              
# def recommend(customer):
#     recommended_items = trained_model[trained_model['CUSTOMER']==customer_id].to_dataframe()
#     print(merge_product_info(recommended_items))
#     visualize_customer_data(get_customer_data(customer_id))

# def analyze(customer):
#     # 

def initialize_model(force = False):
    global initialized, K
    if (not initialized or force == True):
        load_data()
        transactions = get_normilized_data()
        set_model(transactions)
        model.recommend(k=K)
        initialized = True
        print('initialization success!')
    else:
        print('Already initialized')
    return { 'success': True, 'initialized': True }
    

def recommend_items(customer):
    global initialized, model, K
    print('initialized', initialized)
    if (initialized):
        data = merge_with_product_info(model.recommend([customer], k=K).to_dataframe())
        return data
    return { 'sucess': False, 'error': 'Error! not initialized'}

def get_status():
    global initialized
    return { 'sucess': True, 'initialized': initialized }