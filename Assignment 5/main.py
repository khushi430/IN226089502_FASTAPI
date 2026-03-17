
from fastapi import FastAPI

app = FastAPI()

# ------------------ PRODUCTS ------------------

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

# ------------------ ORDERS ------------------

orders = []

# ------------------ Q1 SEARCH ------------------

@app.get("/products/search")
def search_products(keyword: str):
    result = []

    for p in products:
        if keyword.lower() in p["name"].lower():
            result.append(p)

    if not result:
        return {"message": f"No products found for: {keyword}"}

    return {
        "keyword": keyword,
        "total_found": len(result),
        "products": result
    }

# ------------------ Q2 SORT ------------------

@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):

    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False

    sorted_products = sorted(products, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "products": sorted_products
    }

# ------------------ Q3 PAGINATION ------------------

@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):

    total = len(products)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
        "products": products[start:end]
    }

# ------------------ CREATE ORDER ------------------

@app.post("/orders")
def create_order(customer_name: str):
    order_id = len(orders) + 1

    order = {
        "order_id": order_id,
        "customer_name": customer_name
    }

    orders.append(order)

    return {"message": "Order created", "order": order}

# ------------------ Q4 SEARCH ORDERS ------------------

@app.get("/orders/search")
def search_orders(customer_name: str):
    result = []

    for order in orders:
        if customer_name.lower() in order["customer_name"].lower():
            result.append(order)

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }

# ------------------ Q5 SORT BY CATEGORY ------------------

@app.get("/products/sort-by-category")
def sort_by_category():
    sorted_products = sorted(
        products,
        key=lambda x: (x["category"], x["price"])
    )

    return {"products": sorted_products}

# ------------------ Q6 ALL IN ONE ------------------

@app.get("/products/browse")
def browse_products(
    keyword: str = None,
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    data = products

    # SEARCH
    if keyword:
        data = [p for p in data if keyword.lower() in p["name"].lower()]

    # SORT
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    reverse = True if order == "desc" else False
    data = sorted(data, key=lambda x: x[sort_by], reverse=reverse)

    # PAGINATION
    total = len(data)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "total_found": total,
        "total_pages": total_pages,
        "products": data[start:end]
    }

# ------------------ BONUS ------------------

@app.get("/orders/page")
def paginate_orders(page: int = 1, limit: int = 3):
    total = len(orders)
    total_pages = (total + limit - 1) // limit

    start = (page - 1) * limit
    end = start + limit

    return {
        "total_orders": total,
        "total_pages": total_pages,
        "orders": orders[start:end]
    }a

