-- Restaurant Order Management System - Sample Data
-- Populates the database with data from the assessment document

USE RestaurantDB;
GO

-- ================================================================
-- MENU STRUCTURE DATA
-- ================================================================

-- Insert Menus
INSERT INTO menus (menu_id, menu_name) VALUES
(1, 'Food'),
(2, 'Drinks');

-- Insert Categories
INSERT INTO categories (cat_id, category_name, menu_id) VALUES
(1, 'Starters', 1),
(2, 'Soft Drinks', 2),
(3, 'Mains', 1),
(4, 'Desserts', 2),
(5, 'Hot Drinks', 2);

-- Insert Items
INSERT INTO items (item_id, item_name, cat_id, menu_id, has_size_variants) VALUES
(1, 'Item1', 1, 1, 1),  -- Has Small/Large variants
(2, 'Item2', 1, 1, 0),  -- No size variants
(3, 'Item3', 2, 2, 0),
(4, 'Item4', 2, 2, 0),
(5, 'Item5', 2, 1, 0),
(6, 'Item6', 3, 1, 1),  -- Has Small/Large variants
(7, 'Item7', 3, 1, 0),
(8, 'Item8', 4, 2, 1),  -- Has Small/Large variants
(9, 'Item9', 4, 2, 0),
(10, 'Item10', 5, 2, 0);

-- Insert Item Prices (from menu data)
INSERT INTO item_prices (item_id, size, price, is_active) VALUES
(1, 'Small', 1.50, 1),
(1, 'Large', 2.50, 1),
(2, NULL, 3.00, 1),
(3, NULL, 2.50, 1),
(4, NULL, 1.50, 1),
(5, NULL, 1.00, 1),
(6, 'Small', 2.50, 1),
(6, 'Large', 3.60, 1),
(7, NULL, 2.50, 1),
(8, 'Small', 3.75, 1),
(8, 'Large', 6.50, 1),
(9, NULL, 1.50, 1),
(10, NULL, 2.00, 1);

-- ================================================================
-- ORDERS DATA
-- ================================================================

-- Insert Orders (unique order_id values from order history)
INSERT INTO orders (order_id, order_date, order_status) VALUES
(10, '2025-10-01', 'Completed'),
(11, '2025-10-01', 'Completed'),
(12, '2025-10-01', 'Completed'),
(13, '2025-10-01', 'Completed'),
(14, '2025-10-01', 'Completed'),
(15, '2025-10-02', 'Completed'),
(16, '2025-10-03', 'Completed'),
(17, '2025-10-01', 'Completed'),
(18, '2025-10-05', 'Completed'),
(19, '2025-10-01', 'Completed'),
(20, '2025-10-01', 'Completed');

-- ================================================================
-- ORDER ITEMS DATA
-- ================================================================

-- Order 10 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(10, 2, NULL, 2.50, 1, 2.50),
(10, 3, NULL, 1.50, 2, 3.00),
(10, 1, 'Small', 3.75, 1, 3.75);

-- Order 11 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(11, 5, NULL, 2.75, 1, 2.75),
(11, 6, NULL, 1.75, 2, 3.50),
(11, 2, NULL, 2.50, 1, 2.50),
(11, 3, NULL, 3.50, 1, 3.50),
(11, 4, NULL, 3.75, 2, 7.50),
(11, 5, NULL, 1.50, 1, 1.50);

-- Order 12 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(12, 6, 'Large', 5.50, 2, 11.00),
(12, 7, NULL, 2.50, 1, 2.50),
(12, 1, 'Large', 3.50, 1, 3.50);

-- Order 13 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(13, 1, 'Small', 2.75, 2, 5.50),
(13, 6, 'Small', 1.50, 1, 1.50),
(13, 8, 'Small', 3.50, 1, 3.50),
(13, 1, 'Small', 2.50, 2, 5.00);

-- Order 14 items (largest order)
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(14, 6, 'Large', 2.75, 1, 2.75),
(14, 1, 'Large', 2.76, 2, 5.51),
(14, 8, 'Large', 2.75, 2, 5.50),
(14, 1, 'Large', 2.76, 2, 5.51),
(14, 4, NULL, 5.50, 1, 5.50),
(14, 3, NULL, 2.75, 2, 5.50),
(14, 2, NULL, 3.50, 1, 3.50),
(14, 6, 'Large', 3.02, 3, 9.05);

-- Order 15 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(15, 2, NULL, 2.57, 2, 5.14);

-- Order 16 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(16, 6, 'Large', 6.59, 3, 19.76);

-- Order 17 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(17, 10, NULL, 2.50, 1, 2.50),
(17, 9, NULL, 2.76, 1, 2.76),
(17, 7, NULL, 5.64, 1, 5.64);

-- Order 18 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(18, 1, 'Small', 2.57, 2, 5.14),
(18, 6, 'Small', 5.36, 2, 10.72),
(18, 8, 'Small', 5.24, 2, 10.47);

-- Order 19 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(19, 2, NULL, 2.76, 1, 2.76),
(19, 4, NULL, 2.36, 1, 2.36),
(19, 5, NULL, 2.46, 2, 4.91),
(19, 7, NULL, 2.64, 1, 2.64),
(19, 9, NULL, 6.52, 1, 6.52),
(19, 10, NULL, 8.54, 3, 25.62),
(19, 6, 'Large', 5.68, 2, 11.37),
(19, 2, NULL, 6.36, 1, 6.36),
(19, 5, NULL, 7.24, 1, 7.24),
(19, 7, NULL, 2.37, 1, 2.37);

-- Order 20 items
INSERT INTO order_items (order_id, item_id, size, price, quantity, total) VALUES
(20, 1, 'Large', 2.37, 1, 2.37),
(20, 3, NULL, 2.36, 1, 2.36),
(20, 6, 'Large', 1.26, 1, 1.26),
(20, 4, NULL, 2.64, 1, 2.64),
(20, 5, NULL, 5.21, 1, 5.21),
(20, 7, NULL, 6.33, 2, 12.65),
(20, 8, 'Small', 7.25, 1, 7.25),
(20, 9, NULL, 2.40, 1, 2.40),
(20, 4, NULL, 2.36, 3, 7.07),
(20, 6, 'Small', 4.53, 2, 9.07);

-- ================================================================
-- PAYMENTS DATA
-- ================================================================

INSERT INTO payments (payment_id, order_id, payment_date, amount_due, tips, discount, total_paid, payment_type, payment_status) VALUES
(100, 10, '2025-10-01', 9.25, 0, 0, 9.25, 'Card', 'Completed'),
(101, 11, '2025-10-01', 21.25, 0, 0, 10.00, 'Cash', 'Completed'),
(102, 11, '2025-10-01', 21.25, 0, 0, 11.25, 'Card', 'Completed'),
(103, 12, '2025-10-02', 17.00, 3.00, 4.00, 16.00, 'Card', 'Completed'),
(104, 13, '2025-10-03', 15.50, 0, 2.00, 13.50, 'Card', 'Completed'),
(105, 14, '2025-10-01', 42.82, 0, 0, 20.00, 'Cash', 'Completed'),
(106, 14, '2025-10-01', 42.82, 0, 0, 22.82, 'Card', 'Completed'),
(107, 15, '2025-10-02', 5.14, 0, 0, 5.14, 'Card', 'Refunded'),
(108, 16, '2025-10-03', 19.76, 0, 0, 10.00, 'Cash', 'Completed'),
(109, 16, '2025-10-03', 19.76, 0, 0, 9.76, 'Card', 'Completed'),
(110, 17, '2025-10-01', 10.89, 0, 0, 10.90, 'Card', 'Completed'),
(111, 18, '2025-10-05', 26.34, 2.00, 0, 25.00, 'Cash', 'Completed'),
(115, 18, '2025-10-05', 26.34, 0, 0, 3.34, 'Card', 'Completed'),
(116, 19, '2025-10-01', 72.13, 0, 0, 50.00, 'Cash', 'Completed'),
(119, 19, '2025-10-01', 72.13, 0, 0, 22.13, 'Card', 'Completed'),
(120, 20, '2025-10-01', 52.26, 0, 0, 25.00, 'Cash', 'Completed'),
(121, 20, '2025-10-01', 52.26, 0, 0, 27.28, 'Card', 'Completed');

GO

-- ================================================================
-- DATA VERIFICATION QUERIES
-- ================================================================

PRINT 'Sample data inserted successfully!';
PRINT '';
PRINT 'Data Summary:';
PRINT '-------------';

SELECT 'Menus' AS TableName, COUNT(*) AS RecordCount FROM menus
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Items', COUNT(*) FROM items
UNION ALL
SELECT 'Item Prices', COUNT(*) FROM item_prices
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items
UNION ALL
SELECT 'Payments', COUNT(*) FROM payments;

GO
