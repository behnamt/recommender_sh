# Recommender

## Building docker image
````
docker build tk-recommender .
````

## Running the thing
````
docker run -d --network host -name recommender tk-recommender
````

## Using the thing
### Initial data
There should be two files in the init-data directory before initializing the recommender

1. products.csv with columns
    ````
    "SKU": string,
    "IMAGE": string,
    "ATTRIBUTE": stringified json,
    "NAME": string
    ````
2. transactions.csv with columns
    ````
    SKU: string
    CUSTOMER: number
    ````

### Get the status
```
curl -X GET 127.0.0.1:5055/
```
### Initialize the recommender
```
curl -X GET 127.0.0.1:5055/initialize
```
### Get a recommendation for a customer
```
curl -X GET 127.0.0.1:5055/recommend/<customr-reference>
```

### Add a purchase to the recommender
this endpoint should be called every time a purchased is through
```
curl -X POST 127.0.0.1:5055/event/new-purchase --header 'Content-Type: application/json'
--data-raw '{
    "CUSTOMER": 132,
    "SKU": "223423755_1994"
}'
```


### Add a product to the recommender
this endpoint should be called every time a new product is imported
```
curl -X POST 127.0.0.1:5055/event/new-product --header 'Content-Type: application/json'
--data-raw '{
    "NAME": "new pew",
    "SKU": "223423755_1994",
    "IMAGE":"https://link-to-an-image.jpg",
    "ATTRIBUTE": "\"{\"\"color\"\":\"\"milk\"\",\"\"colorCode\"\":1004,\"\"modelCode\"\":224023755,\"\"label\"\":\"\"Svonny\"\",\"\"brand\"\":\"\"OPUS\"\",\"\"keywordCategory\"\":20}\""
}'
```