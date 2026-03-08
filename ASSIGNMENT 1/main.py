from fastapi import FastAPI

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Bluetooth Speaker", "price": 1299, "category": "Electronics", "in_stock": False},
    {"id": 5, "name": "Laptop Stand", "price": 899, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1599, "category": "Electronics", "in_stock": False},
]


@app.get("/")
def home():
    return {"message": "Welcome to My E-commerce Store"}


@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


@app.get("/products/category/{category_name}")
def get_products_by_category(category_name: str):
    filtered_products = [
        product for product in products
        if product["category"].lower() == category_name.lower()
    ]

    if not filtered_products:
        return {"error": "No products found in this category"}

    return {
        "category": category_name,
        "products": filtered_products,
        "total": len(filtered_products)
    }


@app.get("/products/instock")
def get_instock_products():
    in_stock_products = [product for product in products if product["in_stock"]]

    return {
        "in_stock_products": in_stock_products,
        "count": len(in_stock_products)
    }


@app.get("/store/summary")
def get_store_summary():
    total_products = len(products)
    in_stock_count = len([product for product in products if product["in_stock"]])
    out_of_stock_count = total_products - in_stock_count
    categories = list(set(product["category"] for product in products))

    return {
        "store_name": "My E-commerce Store",
        "total_products": total_products,
        "in_stock": in_stock_count,
        "out_of_stock": out_of_stock_count,
        "categories": categories
    }


@app.get("/products/search/{keyword}")
def search_products(keyword: str):
    matched_products = [
        product for product in products
        if keyword.lower() in product["name"].lower()
    ]

    if not matched_products:
        return {"message": "No products matched your search"}

    return {
        "matched_products": matched_products,
        "total": len(matched_products)
    }


@app.get("/products/deals")
def get_product_deals():
    best_deal = min(products, key=lambda product: product["price"])
    premium_pick = max(products, key=lambda product: product["price"])

    return {
        "best_deal": best_deal,
        "premium_pick": premium_pick
    }
