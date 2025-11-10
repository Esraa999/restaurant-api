"""
SQLAlchemy ORM Models
Defines database table structures as Python classes
"""

from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Menu(Base):
    """Menu table - Top level (Food, Drinks)"""
    __tablename__ = "menus"
    
    menu_id = Column(Integer, primary_key=True, index=True)
    menu_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    categories = relationship("Category", back_populates="menu")
    items = relationship("Item", back_populates="menu")


class Category(Base):
    """Categories table - Middle level"""
    __tablename__ = "categories"
    
    cat_id = Column(Integer, primary_key=True, index=True)
    category_name = Column(String(100), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    menu = relationship("Menu", back_populates="categories")
    items = relationship("Item", back_populates="category")


class Item(Base):
    """Items table - Bottom level (Individual menu items)"""
    __tablename__ = "items"
    
    item_id = Column(Integer, primary_key=True, index=True)
    item_name = Column(String(100), nullable=False)
    cat_id = Column(Integer, ForeignKey("categories.cat_id"), nullable=False)
    menu_id = Column(Integer, ForeignKey("menus.menu_id"), nullable=False)
    has_size_variants = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    category = relationship("Category", back_populates="items")
    menu = relationship("Menu", back_populates="items")
    prices = relationship("ItemPrice", back_populates="item")
    order_items = relationship("OrderItem", back_populates="item")


class ItemPrice(Base):
    """Item prices table - Handles size variants and price history"""
    __tablename__ = "item_prices"
    
    price_id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False)
    size = Column(String(20), nullable=True)  # 'Small', 'Large', or NULL
    price = Column(Numeric(10, 2), nullable=False)
    effective_date = Column(DateTime, default=func.now())
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    item = relationship("Item", back_populates="prices")


class Order(Base):
    """Orders table - Order header"""
    __tablename__ = "orders"
    
    order_id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date, nullable=False)
    order_status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    order_items = relationship("OrderItem", back_populates="order")
    payments = relationship("Payment", back_populates="order")


class OrderItem(Base):
    """Order items table - Line items for each order"""
    __tablename__ = "order_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)
    item_id = Column(Integer, ForeignKey("items.item_id"), nullable=False, index=True)
    size = Column(String(20), nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # Price at time of order
    quantity = Column(Integer, nullable=False, default=1)
    total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="order_items")
    item = relationship("Item", back_populates="order_items")


class Payment(Base):
    """Payments table - Payment records for orders"""
    __tablename__ = "payments"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"), nullable=False, index=True)
    payment_date = Column(Date, nullable=False)
    amount_due = Column(Numeric(10, 2), nullable=False)
    tips = Column(Numeric(10, 2), default=0)
    discount = Column(Numeric(10, 2), default=0)
    total_paid = Column(Numeric(10, 2), nullable=False)
    payment_type = Column(String(50), nullable=False)  # 'Cash', 'Card'
    payment_status = Column(String(50), default="Pending")
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    order = relationship("Order", back_populates="payments")
