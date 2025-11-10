"""
Database Configuration Module
Handles database connection and session management
"""

import os
import pyodbc
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Load environment variables
load_dotenv()

# Database configuration from environment
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_NAME = os.getenv("DB_NAME", "RestaurantDB")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "12345678")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")

# Connection string for pyodbc
PYODBC_CONNECTION_STRING = (
    f"DRIVER={{{DB_DRIVER}}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"UID={DB_USER};"
    f"PWD={DB_PASSWORD};"
    "TrustServerCertificate=yes;"
)

# SQLAlchemy connection string
params = quote_plus(PYODBC_CONNECTION_STRING)
SQLALCHEMY_DATABASE_URL = f"mssql+pyodbc:///?odbc_connect={params}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Verify connections before using
    pool_size=5,
    max_overflow=10,
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function for FastAPI to get database sessions
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    """
    Test database connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"✓ Database connection successful!")
            print(f"  Server: {DB_SERVER}")
            print(f"  Database: {DB_NAME}")
            return True
    except Exception as e:
        print(f"✗ Database connection failed!")
        print(f"  Error: {str(e)}")
        return False


def get_pyodbc_connection():
    """
    Get direct pyodbc connection (for raw SQL queries)
    
    Returns:
        pyodbc.Connection: Database connection
    """
    try:
        conn = pyodbc.connect(PYODBC_CONNECTION_STRING)
        return conn
    except Exception as e:
        raise Exception(f"Failed to connect to database: {str(e)}")


if __name__ == "__main__":
    # Test connection when run directly
    test_connection()
