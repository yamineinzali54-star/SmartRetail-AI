from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Product, Customer, Order, OrderItem, Base
from datetime import datetime

app = FastAPI(title="Smart POS API")

engine = create_engine('sqlite:///smart_pos.db')
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Smart POS API is running"}

# ---------- PRODUCTS ----------
@app.get("/products")
def list_products():
    db = SessionLocal()
    products = db.query(Product).all()
    result = [{"product_id": p.product_id, "sku": p.sku, "name": p.product_name,
               "price": p.selling_price, "stock": p.stock_quantity} for p in products]
    db.close()
    return result

@app.post("/products")
def add_product(sku: str, product_name: str, cost_price: float, selling_price: float, stock_quantity: int = 0):
    db = SessionLocal()
    new_product = Product(sku=sku, product_name=product_name, cost_price=cost_price,
                           selling_price=selling_price, stock_quantity=stock_quantity)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    db.close()
    return {"message": "Product added", "product_id": new_product.product_id}

# ---------- CUSTOMERS ----------
@app.get("/customers")
def list_customers():
    db = SessionLocal()
    customers = db.query(Customer).all()
    result = [{"customer_id": c.customer_id, "name": c.customer_name, "type": c.customer_type} for c in customers]
    db.close()
    return result

@app.post("/customers")
def add_customer(customer_code: str, customer_name: str, phone: str = None):
    db = SessionLocal()
    new_customer = Customer(customer_code=customer_code, customer_name=customer_name, phone=phone)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    db.close()
    return {"message": "Customer added", "customer_id": new_customer.customer_id}

# ---------- ORDERS ----------
@app.get("/orders")
def list_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    result = [{"order_id": o.order_id, "order_number": o.order_number,
               "total": o.total_amount, "status": o.order_status} for o in orders]
    db.close()
    return result

@app.post("/orders")
def create_order(order_number: str, subtotal: float, total_amount: float, customer_id: int = None):
    db = SessionLocal()
    new_order = Order(order_number=order_number, subtotal=subtotal, total_amount=total_amount,
                       customer_id=customer_id, order_status='completed')
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    db.close()
    return {"message": "Order created", "order_id": new_order.order_id}