from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "stock": 10},
    {"id": 2, "name": "Notebook", "price": 99, "stock": 20},
    {"id": 3, "name": "USB Hub", "price": 299, "stock": 0},
    {"id": 4, "name": "Pen Set", "price": 49, "stock": 15},
]

cart = []
orders = []
order_id = 1


class Checkout(BaseModel):
    customer_name: str
    delivery_address: str


@app.post("/cart/add")
def add_to_cart(product_id: int, quantity: int = 1):
    product = next((p for p in products if p["id"] == product_id), None)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product["stock"] == 0:
        raise HTTPException(status_code=400, detail=f"{product['name']} is out of stock")

    existing = next((item for item in cart if item["product_id"] == product_id), None)

    if existing:
        existing["quantity"] += quantity
        existing["subtotal"] = existing["quantity"] * product["price"]
        return {"message": "Cart updated", "cart_item": existing}

    item = {
        "product_id": product_id,
        "product_name": product["name"],
        "quantity": quantity,
        "unit_price": product["price"],
        "subtotal": product["price"] * quantity
    }

    cart.append(item)

    return {"message": "Added to cart", "cart_item": item}


@app.get("/cart")
def view_cart():
    if not cart:
        return {"message": "Cart is empty"}

    total = sum(item["subtotal"] for item in cart)

    return {
        "items": cart,
        "item_count": len(cart),
        "grand_total": total
    }


@app.delete("/cart/{product_id}")
def remove_item(product_id: int):
    global cart
    cart = [item for item in cart if item["product_id"] != product_id]
    return {"message": "Item removed from cart"}


@app.post("/cart/checkout")
def checkout(data: Checkout):
    global order_id

    if not cart:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart:
        orders.append({
            "order_id": order_id,
            "customer_name": data.customer_name,
            "product": item["product_name"],
            "quantity": item["quantity"],
            "total": item["subtotal"]
        })
        order_id += 1

    cart.clear()

    return {"message": "Checkout successful"}


@app.get("/orders")
def get_orders():
    return {"orders": orders, "total_orders": len(orders)}
