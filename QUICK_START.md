# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd restaurant-order-api

# Create and activate virtual environment
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 2: Configure Database (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# Update DB_SERVER, DB_USER, and DB_PASSWORD
```

### Step 3: Setup Database (1 minute)

**Option A: Using SSMS**
1. Open SQL Server Management Studio
2. Open and execute `database/schema.sql`
3. Open and execute `database/sample_data.sql`

**Option B: Using Command Line**
```bash
sqlcmd -S localhost -U sa -P YourPassword -i database/schema.sql
sqlcmd -S localhost -U sa -P YourPassword -i database/sample_data.sql
```

### Step 4: Run the API (30 seconds)

```bash
python -m uvicorn app.main:app --reload
```

### Step 5: Test the API (30 seconds)

Open your browser:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Main Endpoint**: http://localhost:8000/api/orders/complete/all

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] SQL Server running
- [ ] Database created successfully
- [ ] Sample data inserted
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] API server running
- [ ] Health check returns "healthy"

---

## 🧪 Quick Test with Postman

1. Import `Restaurant_API.postman_collection.json`
2. Send "Health Check" request
3. Send "Get All Orders (Complete Details)" request
4. Verify response contains orders, items, and payments

---

## 📝 Main Endpoint (Task 2)

```
GET http://localhost:8000/api/orders/complete/all
```

This endpoint returns all orders with:
- Order information
- All order items with menu details
- All payment records
- Calculated totals and balances

---

## ❓ Common Issues

### Database Connection Failed
```bash
# Check SQL Server is running
# Verify credentials in .env
# Test connection: python app/database.py
```

### Port 8000 in Use
```bash
# Use different port
python -m uvicorn app.main:app --reload --port 8001
```

### Module Not Found
```bash
# Make sure virtual environment is activated
# Reinstall: pip install -r requirements.txt
```

---

## 📖 Full Documentation

See [README.md](README.md) for complete documentation including:
- Detailed installation instructions
- API endpoint documentation
- Security features
- Performance optimizations
- Data analysis findings

---

**Ready to Demo! 🎉**
