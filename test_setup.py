"""
Test Script - Verify Database and API Setup
Run this script to test if everything is configured correctly
"""

import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required packages are installed"""
    print("=" * 60)
    print("Testing Package Imports...")
    print("=" * 60)
    
    packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('pyodbc', 'PyODBC'),
        ('pydantic', 'Pydantic'),
        ('dotenv', 'python-dotenv')
    ]
    
    failed = []
    for package, name in packages:
        try:
            __import__(package)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} NOT installed")
            failed.append(name)
    
    if failed:
        print(f"\n⚠️ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required packages installed!")
        return True


def test_database():
    """Test database connection"""
    print("\n" + "=" * 60)
    print("Testing Database Connection...")
    print("=" * 60)
    
    try:
        from app.database import test_connection
        
        if test_connection():
            print("\n✓ Database connection successful!")
            return True
        else:
            print("\n✗ Database connection failed!")
            print("\nTroubleshooting:")
            print("1. Check if SQL Server is running")
            print("2. Verify credentials in .env file")
            print("3. Run database setup scripts:")
            print("   sqlcmd -S localhost -U sa -P YourPass -i database/schema.sql")
            print("   sqlcmd -S localhost -U sa -P YourPass -i database/sample_data.sql")
            return False
            
    except Exception as e:
        print(f"\n✗ Error testing database: {str(e)}")
        return False


def test_data():
    """Test if sample data exists"""
    print("\n" + "=" * 60)
    print("Testing Sample Data...")
    print("=" * 60)
    
    try:
        from app.database import get_db
        from app.models import Order, Item, Payment
        from sqlalchemy import func
        
        db = next(get_db())
        
        # Count records
        order_count = db.query(func.count(Order.order_id)).scalar()
        item_count = db.query(func.count(Item.item_id)).scalar()
        payment_count = db.query(func.count(Payment.payment_id)).scalar()
        
        print(f"Orders: {order_count}")
        print(f"Items: {item_count}")
        print(f"Payments: {payment_count}")
        
        if order_count >= 11 and item_count >= 10 and payment_count >= 17:
            print("\n✓ Sample data loaded successfully!")
            return True
        else:
            print("\n⚠️ Sample data incomplete!")
            print("Expected: 11 orders, 10 items, 17 payments")
            print("Run: sqlcmd -S localhost -U sa -P YourPass -i database/sample_data.sql")
            return False
            
    except Exception as e:
        print(f"\n✗ Error checking data: {str(e)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("RESTAURANT ORDER API - SETUP VERIFICATION")
    print("=" * 60)
    
    results = []
    
    # Test imports
    results.append(("Package Imports", test_imports()))
    
    # Test database only if imports successful
    if results[0][1]:
        results.append(("Database Connection", test_database()))
        
        # Test data only if database connected
        if results[1][1]:
            results.append(("Sample Data", test_data()))
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nYou can now start the API server:")
        print("  python -m uvicorn app.main:app --reload")
        print("\nThen open:")
        print("  http://localhost:8000/docs")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("⚠️ SOME TESTS FAILED")
        print("=" * 60)
        print("\nPlease fix the issues above before running the API.")
        print("See README.md for detailed setup instructions.")
        print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
