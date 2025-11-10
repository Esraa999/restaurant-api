"""
Pydantic Schemas
Defines request and response models for API validation and documentation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal


# ================================================================
# MENU SCHEMAS
# ================================================================

class MenuBase(BaseModel):
    menu_name: str = Field(..., description="Name of the menu")


class MenuResponse(MenuBase):
    menu_id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# ================================================================
# CATEGORY SCHEMAS
# ================================================================

class CategoryBase(BaseModel):
    category_name: str
    menu_id: int


class CategoryResponse(CategoryBase):
    cat_id: int
    
    model_config = ConfigDict(from_attributes=True)


# ================================================================
# ITEM SCHEMAS
# ================================================================

class ItemPriceResponse(BaseModel):
    price_id: int
    size: Optional[str] = None
    price: Decimal
    is_active: bool
    
    model_config = ConfigDict(from_attributes=True)


class ItemResponse(BaseModel):
    item_id: int
    item_name: str
    cat_id: int
    menu_id: int
    has_size_variants: bool
    category_name: Optional[str] = None
    menu_name: Optional[str] = None
    prices: List[ItemPriceResponse] = []
    
    model_config = ConfigDict(from_attributes=True)


# ================================================================
# ORDER ITEM SCHEMAS
# ================================================================

class OrderItemResponse(BaseModel):
    id: int
    item_id: int
    item_name: str
    category_name: str
    menu_name: str
    size: Optional[str] = None
    price: Decimal = Field(..., description="Price at time of order")
    quantity: int
    total: Decimal = Field(..., description="Line item total (price × quantity)")
    
    model_config = ConfigDict(from_attributes=True)


# ================================================================
# PAYMENT SCHEMAS
# ================================================================

class PaymentResponse(BaseModel):
    payment_id: int
    payment_date: date
    amount_due: Decimal
    tips: Decimal
    discount: Decimal
    total_paid: Decimal
    payment_type: str = Field(..., description="Cash or Card")
    payment_status: str = Field(..., description="Completed, Pending, or Refunded")
    
    model_config = ConfigDict(from_attributes=True)


# ================================================================
# ORDER SCHEMAS
# ================================================================

class OrderSummary(BaseModel):
    """Simplified order response for list views"""
    order_id: int
    order_date: date
    order_status: str
    total_items: int = Field(..., description="Number of line items")
    order_total: Decimal = Field(..., description="Sum of all order items")
    total_payments: Decimal = Field(..., description="Sum of all payments")
    payment_balance: Decimal = Field(..., description="Amount still due (can be negative)")
    
    model_config = ConfigDict(from_attributes=True)


class OrderDetailResponse(BaseModel):
    """Complete order response with all related data"""
    order_id: int
    order_date: date
    order_status: str
    created_at: Optional[datetime] = None
    
    # Order items
    items: List[OrderItemResponse] = Field(default_factory=list)
    
    # Payments
    payments: List[PaymentResponse] = Field(default_factory=list)
    
    # Calculated fields
    total_items_count: int = Field(..., description="Total number of line items")
    order_subtotal: Decimal = Field(..., description="Sum of all item totals")
    total_paid: Decimal = Field(..., description="Sum of all payment amounts")
    payment_balance: Decimal = Field(..., description="Remaining balance (negative = overpaid)")
    
    model_config = ConfigDict(from_attributes=True)


# ================================================================
# API RESPONSE WRAPPERS
# ================================================================

class SuccessResponse(BaseModel):
    """Standard success response wrapper"""
    success: bool = True
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper"""
    success: bool = False
    error: str
    detail: Optional[str] = None


class PaginatedResponse(BaseModel):
    """Paginated response wrapper"""
    success: bool = True
    total: int
    page: int
    page_size: int
    total_pages: int
    data: List[dict]
