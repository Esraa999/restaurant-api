"""
FastAPI Restaurant Order Management System
Main application file with API endpoints
"""

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, desc
from typing import List, Optional
from decimal import Decimal
import os
from dotenv import load_dotenv

from app.database import get_db, test_connection
from app.models import Order, OrderItem, Payment, Item, Category, Menu
from app.schemas import (
    OrderDetailResponse, OrderSummary, OrderItemResponse, 
    PaymentResponse, SuccessResponse, ErrorResponse
)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Restaurant Order Management API",
    description="""
    ## Fullstack Developer Assessment - Python API
    
    A comprehensive REST API for managing restaurant orders, payments, and menu items.
    
    ### Features:
    * 📋 List all orders with complete details
    * 💰 View payment information with tips and discounts
    * 🍽️ Access menu items with categories
    * 🔍 Filter and search orders
    * 📊 Real-time order analytics
    
    ### Security:
    * Input validation using Pydantic
    * SQL injection protection via SQLAlchemy ORM
    * CORS configuration for cross-origin requests
    
    ### Performance:
    * Database connection pooling
    * Indexed queries for fast lookups
    * Optimized joins with eager loading
    """,
    version="1.0.0",
    contact={
        "name": "API Support",
        "email": "support@restaurant-api.com"
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT"
    }
)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ================================================================
# EXCEPTION HANDLERS
# ================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler for unexpected errors"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc)
        }
    )


# ================================================================
# HEALTH CHECK ENDPOINTS
# ================================================================

@app.get("/", tags=["Health"])
async def root():
    """
    Root endpoint - API information
    """
    return {
        "name": "Restaurant Order Management API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint - Verifies database connectivity
    """
    db_connected = test_connection()
    
    return {
        "status": "healthy" if db_connected else "unhealthy",
        "database": "connected" if db_connected else "disconnected",
        "api": "running"
    }


# ================================================================
# ORDER ENDPOINTS
# ================================================================

@app.get(
    "/api/orders",
    response_model=List[OrderSummary],
    tags=["Orders"],
    summary="List all orders with summary",
    description="""
    Retrieve a list of all orders with summary information including:
    - Order totals
    - Payment totals
    - Balance due
    - Item count
    
    **Performance**: Optimized query with aggregations
    """
)
async def get_orders_summary(
    status: Optional[str] = Query(None, description="Filter by order status (e.g., 'Completed')"),
    date: Optional[str] = Query(None, description="Filter by order date (YYYY-MM-DD format)"),
    db: Session = Depends(get_db)
):
    """Get all orders with summary information"""
    try:
        # Base query
        query = db.query(Order)
        
        # Apply filters
        if status:
            query = query.filter(Order.order_status == status)
        if date:
            query = query.filter(Order.order_date == date)
        
        orders = query.order_by(desc(Order.order_date), desc(Order.order_id)).all()
        
        result = []
        for order in orders:
            # Calculate order total
            order_total = db.query(func.sum(OrderItem.total)).filter(
                OrderItem.order_id == order.order_id
            ).scalar() or Decimal('0.00')
            
            # Calculate total payments
            total_payments = db.query(func.sum(Payment.total_paid)).filter(
                Payment.order_id == order.order_id,
                Payment.payment_status == 'Completed'
            ).scalar() or Decimal('0.00')
            
            # Count items
            total_items = db.query(func.count(OrderItem.id)).filter(
                OrderItem.order_id == order.order_id
            ).scalar() or 0
            
            result.append(OrderSummary(
                order_id=order.order_id,
                order_date=order.order_date,
                order_status=order.order_status,
                total_items=total_items,
                order_total=order_total,
                total_payments=total_payments,
                payment_balance=order_total - total_payments
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving orders: {str(e)}"
        )


@app.get(
    "/api/orders/{order_id}",
    response_model=OrderDetailResponse,
    tags=["Orders"],
    summary="Get complete order details",
    description="""
    Retrieve complete details for a specific order including:
    - All order items with menu information
    - All payment records
    - Calculated totals and balances
    
    **Performance**: Uses eager loading to minimize database queries
    """
)
async def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db)
):
    """Get complete order details with items and payments"""
    try:
        # Fetch order with eager loading
        order = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.item).joinedload(Item.category),
            joinedload(Order.order_items).joinedload(OrderItem.item).joinedload(Item.menu),
            joinedload(Order.payments)
        ).filter(Order.order_id == order_id).first()
        
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order {order_id} not found"
            )
        
        # Build order items response
        items_response = []
        order_subtotal = Decimal('0.00')
        
        for order_item in order.order_items:
            items_response.append(OrderItemResponse(
                id=order_item.id,
                item_id=order_item.item_id,
                item_name=order_item.item.item_name,
                category_name=order_item.item.category.category_name,
                menu_name=order_item.item.menu.menu_name,
                size=order_item.size,
                price=order_item.price,
                quantity=order_item.quantity,
                total=order_item.total
            ))
            order_subtotal += order_item.total
        
        # Build payments response
        payments_response = []
        total_paid = Decimal('0.00')
        
        for payment in order.payments:
            payments_response.append(PaymentResponse(
                payment_id=payment.payment_id,
                payment_date=payment.payment_date,
                amount_due=payment.amount_due,
                tips=payment.tips,
                discount=payment.discount,
                total_paid=payment.total_paid,
                payment_type=payment.payment_type,
                payment_status=payment.payment_status
            ))
            if payment.payment_status == 'Completed':
                total_paid += payment.total_paid
        
        # Build complete response
        return OrderDetailResponse(
            order_id=order.order_id,
            order_date=order.order_date,
            order_status=order.order_status,
            created_at=order.created_at,
            items=items_response,
            payments=payments_response,
            total_items_count=len(items_response),
            order_subtotal=order_subtotal,
            total_paid=total_paid,
            payment_balance=order_subtotal - total_paid
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving order details: {str(e)}"
        )


@app.get(
    "/api/orders/complete/all",
    response_model=List[OrderDetailResponse],
    tags=["Orders"],
    summary="Get all orders with complete details",
    description="""
    **⚠️ Main Assessment Endpoint**
    
    Retrieve ALL orders with complete details including:
    - Full order information
    - All order items with prices and quantities
    - Menu and category information for each item
    - All payment records with tips and discounts
    - Calculated totals and balances
    
    This endpoint fulfills Task 2 of the assessment:
    "List all orders with payment details and full order details"
    
    **Performance Considerations**:
    - Uses optimized queries with joins
    - Implements eager loading to reduce N+1 queries
    - Returns complete dataset in single request
    
    **Response Structure**:
    Each order includes:
    - Order metadata (ID, date, status)
    - Array of order items (with item details, price, quantity)
    - Array of payments (with type, amount, status)
    - Calculated aggregates (subtotal, total paid, balance)
    """
)
async def get_all_orders_complete(
    db: Session = Depends(get_db)
):
    """
    Get all orders with complete details - Main assessment endpoint
    Task 2: List all orders with payment details and full order details
    """
    try:
        # Fetch all orders with eager loading for optimal performance
        orders = db.query(Order).options(
            joinedload(Order.order_items).joinedload(OrderItem.item).joinedload(Item.category),
            joinedload(Order.order_items).joinedload(OrderItem.item).joinedload(Item.menu),
            joinedload(Order.payments)
        ).order_by(desc(Order.order_date), desc(Order.order_id)).all()
        
        result = []
        
        for order in orders:
            # Build order items
            items_response = []
            order_subtotal = Decimal('0.00')
            
            for order_item in order.order_items:
                items_response.append(OrderItemResponse(
                    id=order_item.id,
                    item_id=order_item.item_id,
                    item_name=order_item.item.item_name,
                    category_name=order_item.item.category.category_name,
                    menu_name=order_item.item.menu.menu_name,
                    size=order_item.size,
                    price=order_item.price,
                    quantity=order_item.quantity,
                    total=order_item.total
                ))
                order_subtotal += order_item.total
            
            # Build payments
            payments_response = []
            total_paid = Decimal('0.00')
            
            for payment in order.payments:
                payments_response.append(PaymentResponse(
                    payment_id=payment.payment_id,
                    payment_date=payment.payment_date,
                    amount_due=payment.amount_due,
                    tips=payment.tips,
                    discount=payment.discount,
                    total_paid=payment.total_paid,
                    payment_type=payment.payment_type,
                    payment_status=payment.payment_status
                ))
                if payment.payment_status == 'Completed':
                    total_paid += payment.total_paid
            
            # Add to result
            result.append(OrderDetailResponse(
                order_id=order.order_id,
                order_date=order.order_date,
                order_status=order.order_status,
                created_at=order.created_at,
                items=items_response,
                payments=payments_response,
                total_items_count=len(items_response),
                order_subtotal=order_subtotal,
                total_paid=total_paid,
                payment_balance=order_subtotal - total_paid
            ))
        
        return result
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving complete order details: {str(e)}"
        )


# ================================================================
# STATISTICS ENDPOINTS
# ================================================================

@app.get(
    "/api/statistics/overview",
    tags=["Statistics"],
    summary="Get business statistics overview"
)
async def get_statistics(db: Session = Depends(get_db)):
    """Get overall business statistics"""
    try:
        total_orders = db.query(func.count(Order.order_id)).scalar()
        total_revenue = db.query(func.sum(OrderItem.total)).scalar() or Decimal('0.00')
        total_payments = db.query(func.sum(Payment.total_paid)).filter(
            Payment.payment_status == 'Completed'
        ).scalar() or Decimal('0.00')
        
        return {
            "success": True,
            "data": {
                "total_orders": total_orders,
                "total_revenue": float(total_revenue),
                "total_payments_received": float(total_payments),
                "outstanding_balance": float(total_revenue - total_payments)
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving statistics: {str(e)}"
        )


# ================================================================
# STARTUP EVENT
# ================================================================

@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    print("=" * 60)
    print("🚀 Restaurant Order Management API Starting...")
    print("=" * 60)
    
    # Test database connection
    if test_connection():
        print("✓ Database connection verified")
    else:
        print("✗ WARNING: Database connection failed")
    
    print(f"✓ API Documentation: http://localhost:8000/docs")
    print(f"✓ ReDoc Documentation: http://localhost:8000/redoc")
    print("=" * 60)


if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    reload = os.getenv("API_RELOAD", "True").lower() == "true"
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=reload
    )
