#!/bin/bash

echo "============================================================"
echo "Restaurant Order Management API - Startup Script"
echo "============================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "ERROR: Virtual environment not found!"
    echo "Please run: python -m venv venv"
    echo "Then activate it and install requirements."
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment!"
    exit 1
fi

echo "Virtual environment activated successfully!"
echo ""

# Run the API server
echo "Starting API server..."
echo ""
echo "API will be available at:"
echo "  - Interactive Docs: http://localhost:8000/docs"
echo "  - ReDoc: http://localhost:8000/redoc"
echo "  - Health Check: http://localhost:8000/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo "============================================================"
echo ""

python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
