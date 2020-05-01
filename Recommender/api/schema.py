product_schema = {
    "type": "object",
    "properties": {
        "sku": { "type": "string" },
        "image": { "type": "string" },
        "attribute": { "type": "string" },
        "name": { "type": "string" }
    }
}

purchase_schema = {
    "type": "object",
    "properties": {
        "customer": { "type": "number" },
        "sku": { "type": "string" }
    }
}