from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String, unique=True, nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String)
    brand = Column(String)
    unit = Column(String)
    cost_price = Column(Float, nullable=False)
    selling_price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    reorder_level = Column(Integer, default=10)
    supplier_name = Column(String)
    status = Column(String, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('stock_quantity >= 0', name='check_stock_non_negative'),
        CheckConstraint('reorder_level >= 0', name='check_reorder_non_negative'),
    )

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True, autoincrement=True)
    customer_code = Column(String, unique=True, nullable=False)
    customer_name = Column(String, nullable=False)
    phone = Column(String, index=True)
    email = Column(String, index=True)
    gender = Column(String)
    date_of_birth = Column(DateTime)
    address = Column(String)
    customer_type = Column(String, default='regular')
    status = Column(String, default='active')
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    order_number = Column(String, unique=True, nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    order_date = Column(DateTime, default=datetime.utcnow, index=True)
    subtotal = Column(Float, nullable=False)
    discount_amount = Column(Float, default=0)
    tax_amount = Column(Float, default=0)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String)
    payment_status = Column(String, default='unpaid')
    order_status = Column(String, default='pending', index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("OrderItem", back_populates="order")

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='check_total_non_negative'),
    )

class OrderItem(Base):
    __tablename__ = 'order_items'
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('orders.order_id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.product_id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # actual price at time of sale
    discount_amount = Column(Float, default=0)
    subtotal = Column(Float, nullable=False)
    total_amount = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    order = relationship("Order", back_populates="items")

    __table_args__ = (
        CheckConstraint('quantity > 0', name='check_quantity_positive'),
    )

# SQLite database file ဆောက်ခြင်း
engine = create_engine('sqlite:///smart_pos.db', echo=True)
Base.metadata.create_all(engine)

print("Database created successfully: smart_pos.db")