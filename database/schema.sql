-- Restaurant Order Management System Database Schema
-- Database: RestaurantDB
-- MSSQL Server Compatible

USE master;
GO

-- Drop database if exists
IF EXISTS (SELECT name FROM sys.databases WHERE name = 'RestaurantDB')
BEGIN
    ALTER DATABASE RestaurantDB SET SINGLE_USER WITH ROLLBACK IMMEDIATE;
    DROP DATABASE RestaurantDB;
END
GO

-- Create database
CREATE DATABASE RestaurantDB;
GO

USE RestaurantDB;
GO

-- ================================================================
-- MENU STRUCTURE TABLES
-- ================================================================

-- Menus table (Top level: Food, Drinks)
CREATE TABLE menus (
    menu_id INT PRIMARY KEY,
    menu_name NVARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Categories table (Middle level: Starters, Mains, etc.)
CREATE TABLE categories (
    cat_id INT PRIMARY KEY,
    category_name NVARCHAR(100) NOT NULL,
    menu_id INT NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
);

-- Items table (Bottom level: Individual items)
CREATE TABLE items (
    item_id INT PRIMARY KEY,
    item_name NVARCHAR(100) NOT NULL,
    cat_id INT NOT NULL,
    menu_id INT NOT NULL,
    has_size_variants BIT DEFAULT 0,
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (cat_id) REFERENCES categories(cat_id),
    FOREIGN KEY (menu_id) REFERENCES menus(menu_id)
);

-- Item prices table (handles size variants and price history)
CREATE TABLE item_prices (
    price_id INT PRIMARY KEY IDENTITY(1,1),
    item_id INT NOT NULL,
    size NVARCHAR(20) NULL, -- 'Small', 'Large', or NULL for standard
    price DECIMAL(10, 2) NOT NULL,
    effective_date DATETIME DEFAULT GETDATE(),
    is_active BIT DEFAULT 1,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- ================================================================
-- ORDER TABLES
-- ================================================================

-- Orders table (header)
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    order_status NVARCHAR(50) DEFAULT 'Pending',
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE()
);

-- Order items table (line items)
CREATE TABLE order_items (
    id INT PRIMARY KEY IDENTITY(1,1),
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    size NVARCHAR(20) NULL,
    price DECIMAL(10, 2) NOT NULL, -- Price at time of order
    quantity INT NOT NULL DEFAULT 1,
    total DECIMAL(10, 2) NOT NULL,
    created_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id) REFERENCES items(item_id)
);

-- ================================================================
-- PAYMENT TABLES
-- ================================================================

-- Payments table
CREATE TABLE payments (
    payment_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    payment_date DATE NOT NULL,
    amount_due DECIMAL(10, 2) NOT NULL,
    tips DECIMAL(10, 2) DEFAULT 0,
    discount DECIMAL(10, 2) DEFAULT 0,
    total_paid DECIMAL(10, 2) NOT NULL,
    payment_type NVARCHAR(50) NOT NULL, -- 'Cash', 'Card'
    payment_status NVARCHAR(50) DEFAULT 'Pending',
    created_at DATETIME DEFAULT GETDATE(),
    updated_at DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- ================================================================
-- INDEXES FOR PERFORMANCE
-- ================================================================

-- Orders indexes
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_orders_status ON orders(order_status);

-- Order items indexes
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_item_id ON order_items(item_id);

-- Payments indexes
CREATE INDEX idx_payments_order_id ON payments(order_id);
CREATE INDEX idx_payments_date ON payments(payment_date);
CREATE INDEX idx_payments_status ON payments(payment_status);

-- Item prices indexes
CREATE INDEX idx_item_prices_item_id ON item_prices(item_id);
CREATE INDEX idx_item_prices_active ON item_prices(is_active);

GO

PRINT 'Database schema created successfully!';
