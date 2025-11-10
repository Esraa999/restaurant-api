# Task 1: Data Analysis Findings

## Executive Summary
This document presents a comprehensive analysis of the restaurant order management system data, including menu structure, order history, and payment information.

---

## 1. Data Structure Overview

### 1.1 Menu Data Structure
The menu follows a **hierarchical three-level structure**:
- **Menu Level** (Top): Food vs Drinks
- **Category Level** (Middle): Starters, Mains, Soft Drinks, Desserts, Hot Drinks
- **Item Level** (Bottom): Individual menu items

**Key Observations:**
- 10 unique items across 5 categories
- 2 main menus (Food and Drinks)
- Items can have size variants (Small/Large) with different pricing
- Some items have no size specification (standard size)

### 1.2 Order History Structure
- **53 order line items** across **11 unique orders** (Order IDs: 10-20)
- Date range: October 1-5, 2025
- All orders have "Completed" status

### 1.3 Payment Structure
- **17 payment records** for the 11 orders
- Multiple payment methods: Cash and Card
- One refunded payment (Payment ID 107 for Order 15)

---

## 2. Critical Data Quality Issues

### 2.1 **CRITICAL: Price Inconsistencies**
The most significant issue is **inconsistent pricing for the same item**:

**Item 1 (Small) Price Variations:**
- Menu price: 1.50
- Order History shows: 3.75, 2.75, 2.5, 2.7556, 2.75655, 2.5698, 2.3658

**Item 6 (Large) Price Variations:**
- Menu price: 3.6
- Order History shows: 5.5, 2.75, 3.015, 6.586, 5.683, 1.256, 4.5326

**Possible Causes:**
1. Dynamic pricing based on time/demand
2. Promotions or discounts applied at order level
3. Data entry errors
4. Menu price updates not reflected historically
5. Special pricing for certain customers

**Business Impact:** This makes revenue analysis and profit margin calculations unreliable.

---

### 2.2 Missing Size Information
Many order records have **blank "Size" fields** despite items supporting multiple sizes:
- Item 1: 4 out of 13 records missing size
- Item 6: 2 out of 10 records missing size
- Item 8: 1 out of 3 records missing size

**Issue:** Cannot determine which variant was ordered, affecting inventory and pricing accuracy.

---

### 2.3 Data Type Inconsistencies
- **Price field**: Contains high-precision decimal values (e.g., 2.75655, 5.63982)
- **Typical restaurant pricing**: Usually 2 decimal places
- **Implication**: Potential floating-point calculation artifacts or currency conversion

---

## 3. Database Relationship Analysis

### 3.1 Identified Relationships

```
Menu (1) ----< Category (Many)
Category (1) ----< Item (Many)
Order (1) ----< OrderItem (Many)
Item (1) ----< OrderItem (Many)
Order (1) ----< Payment (Many)
```

### 3.2 Referential Integrity Issues

**Orders without Payment Records:**
- Order 15 has payment, but it's marked as "Refunded"
- This creates ambiguity: Is the order truly completed?

**Menu Item Mismatches:**
- Menu defines prices, but orders show different prices
- No audit trail to explain discrepancies

---

## 4. Business Logic Findings

### 4.1 Order Patterns

**Order Size Distribution:**
- Small orders: 3 items (Order 10)
- Large orders: 13 items (Order 20)
- Average: ~4.8 items per order

**Popular Items (by frequency):**
1. Item 6: 10 occurrences
2. Item 1: 13 occurrences
3. Item 2: 6 occurrences
4. Item 4: 4 occurrences

### 4.2 Payment Patterns

**Split Payments:**
- 6 orders have **multiple payments** (mixed Cash + Card)
- Example: Order 11 split into 10.00 (Cash) + 11.25 (Card)
- Order 14: Largest split with 20.00 (Cash) + 22.82 (Card)

**Payment Status:**
- 1 refunded payment (Order 15: 5.14 Card)
- 16 completed payments

**Payment Coverage Analysis:**
```
Order 10: Amount Due 9.25, Paid 9.25 ✓ (100%)
Order 11: Amount Due 21.25, Paid 21.25 ✓ (100%)
Order 12: Amount Due 17.00, Paid 16.00 (with tips & discount) ✓
Order 14: Amount Due 42.82, Paid 42.82 ✓ (100%)
```

**Issue Detected:**
Order 15 was refunded but still shows as "Completed" in order status.

---

## 5. Data Validation Issues

### 5.1 Total Price Calculation Errors
Spot-checking reveals calculation mismatches:

**Order 10:**
- Item 2: Price 2.5 × Qty 1 = 2.5 ✓
- Item 3: Price 1.5 × Qty 2 = 3.0 ✓
- Item 1: Price 3.75 × Qty 1 = 3.75 ✓
- **Total should be:** 9.25 ✓

**Order 14 (with inconsistent prices):**
- Multiple items with unusual prices (2.75655, 3.015, etc.)
- Total: 42.8193
- **Concern:** Precision suggests system calculation, but source unclear

---

## 6. Recommendations for Data Structure

### 6.1 Database Schema Improvements

**Suggested Tables:**
1. **menus** (id, name)
2. **categories** (id, name, menu_id)
3. **items** (id, name, category_id)
4. **item_prices** (id, item_id, size, price, effective_date) ← **New table for price history**
5. **orders** (id, order_date, status, created_at)
6. **order_items** (id, order_id, item_id, size, price_at_order, quantity, total)
7. **payments** (id, order_id, payment_date, amount, tips, discount, total_paid, type, status)

**Key Addition:** 
- `item_prices` table with `effective_date` to track historical pricing
- `price_at_order` field in `order_items` to preserve pricing at time of sale

### 6.2 Data Validation Rules

1. **Order Total = Sum of OrderItem Totals**
2. **Payment Total = Amount Due - Discount + Tips**
3. **Size field mandatory** if item has size variants
4. **Price precision:** Standardize to 2 decimal places
5. **Payment validation:** Sum of payments ≥ Amount Due

---

## 7. Business Questions to Clarify

1. **Pricing Strategy:**
   - Why do prices vary from menu prices?
   - Is dynamic pricing intentional?
   - How are discounts applied?

2. **Size Handling:**
   - What happens when size is not specified?
   - Should system default to standard size?

3. **Payment Logic:**
   - Why are large orders often split between Cash/Card?
   - What is the refund policy?
   - Should refunded orders maintain "Completed" status?

4. **Menu Management:**
   - How often do prices change?
   - Is there a price history requirement?
   - Are promotional prices tracked separately?

---

## 8. Data Relevancy & Combinations

### 8.1 Useful Data Combinations

**For Sales Analysis:**
```sql
Orders + OrderItems + Items + Categories + Menus
→ Reveals best-selling categories and revenue by menu type
```

**For Financial Reconciliation:**
```sql
Orders + Payments
→ Tracks payment completeness and refunds
```

**For Pricing Analysis:**
```sql
OrderItems.price_at_order vs Items.current_price
→ Identifies pricing trends and discount patterns
```

### 8.2 Missing Data Points

**Customer Information:**
- No customer ID or contact info
- Cannot track repeat customers
- No loyalty program data

**Operational Data:**
- No table numbers
- No server/staff ID
- No order preparation time
- No delivery method

**Inventory Data:**
- No ingredient tracking
- No cost of goods sold (COGS)
- Cannot calculate profit margins

---

## 9. Technical Implementation Notes

### 9.1 API Design Implications

**Required Joins:**
- List orders: Need to join Orders → OrderItems → Items → Categories
- Include payments: Join Orders → Payments

**Performance Considerations:**
- Index on order_id in order_items and payments
- Index on item_id in order_items
- Consider caching menu data

**Data Integrity:**
- Validate order totals before saving
- Enforce foreign key constraints
- Implement soft deletes for auditability

### 9.2 Security Considerations

- **PII Protection:** No sensitive customer data visible (good)
- **Payment Data:** Ensure PCI compliance if storing card details
- **Access Control:** Implement role-based access for financial data

---

## 10. Conclusion

The dataset reveals a functional restaurant order system with several **critical data quality issues**:

### Strengths:
✓ Clear hierarchical menu structure  
✓ Complete order lifecycle tracking  
✓ Multiple payment method support  
✓ All orders marked as completed  

### Critical Issues:
✗ **Inconsistent pricing** (highest priority to address)  
✗ Missing size information  
✗ No price history tracking  
✗ Refunded order status ambiguity  

### Next Steps:
1. Implement price history table
2. Enforce size selection for variant items
3. Add data validation rules
4. Create price audit trail
5. Standardize decimal precision

This analysis provides the foundation for building a robust Python API with proper data validation and business logic enforcement.
