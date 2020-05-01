import pandas as ps

TRANSACTIONS_SAVE_PATH = "data/transactions.pkl"
TRANSACTIONS_INITIAL_LOAD_PATH = "init-data/transactions.csv"

PRODUCTS_SAVE_PATH = "data/products.pkl"
PRODUCTS_INITIAL_LOAD_PATH = "init-data/products.csv"


def load_transactions():
    # read transactions
    try:
        transactions_raw = ps.read_pickle(TRANSACTIONS_SAVE_PATH)
        print('Loaded transactions from pickle')
    except FileNotFoundError:
        try:
            transactions_raw = ps.read_csv(TRANSACTIONS_INITIAL_LOAD_PATH, names = ['SKU', 'CUSTOMER'], header = 1)
            transactions_raw.to_pickle(TRANSACTIONS_SAVE_PATH)
            print('Loaded transactions from csv file')
        except:
            raise Exception("Cannot load the transactions csv file")
    return transactions_raw

def load_products():
    # read products
    try:
        products_raw = ps.read_pickle(PRODUCTS_SAVE_PATH)
        print('Loaded products from pickle')
    except FileNotFoundError:
        try:
            products_raw = ps.read_csv(PRODUCTS_INITIAL_LOAD_PATH)
            products_raw.to_pickle(PRODUCTS_SAVE_PATH)
            print('Loaded products from csv file')
        except:
            raise Exception("Cannot load the products csv file")
    return products_raw
    
def load_raw_data():
    return load_transactions(), load_products()

def save_transactions(_transactions):
    _transactions.to_pickle(TRANSACTIONS_SAVE_PATH)

def save_products(_products):
    _products.to_pickle(PRODUCTS_SAVE_PATH)
