# Invoice System Logic Documentation

## Overview
This document provides a comprehensive guide for implementing a custom backend API to handle invoice operations in the Tantawy system. The system supports four types of invoices with different accounting behaviors and transaction patterns.

## Invoice Types
1. **Purchase Invoice** (Type: 1) - Recording purchases from vendors
2. **Sales Invoice** (Type: 2) - Recording sales to customers  
3. **Return Purchase Invoice** (Type: 3) - Recording returns to vendors
4. **Return Sales Invoice** (Type: 4) - Recording returns from customers

## Database Tables Required

### 1. invoiceMaster Table
**Purpose**: Stores the main invoice header information

**Required Fields**:
- `id` (Primary Key, Auto-increment)
- `invoiceType` (Integer: 1=Purchase, 2=Sales, 3=Return Purchase, 4=Return Sales)
- `customerOrVendorID` (Foreign Key to customer/vendor)
- `storeId` (Foreign Key to store/location)
- `status` (Integer: Invoice status)
- `paymentType` (Integer: 1=Cash, 2=Visa, 3=Deferred)
- `notes` (String: Additional notes)
- `discountAmount` (Decimal: Total discount in currency)
- `discountPercentage` (Decimal: Total discount percentage)
- `taxAmount` (Decimal: Total tax in currency)
- `taxPercentage` (Decimal: Total tax percentage)
- `netTotal` (Decimal: Final total amount)
- `totalPaid` (Decimal: Amount already paid)
- `returnStatus` (Integer: Return processing status)
- `originalInvoiceID` (Foreign Key: Reference to original invoice for returns)
- `createdBy` (Integer: User ID who created)
- `createdOn` (DateTime: Creation timestamp)
- `updatedBy` (Integer: User ID who last updated)
- `updatedOn` (DateTime: Last update timestamp)
- `deletedBy` (Integer: User ID who deleted)
- `deletedOn` (DateTime: Deletion timestamp)
- `isDeleted` (Boolean: Soft delete flag)

### 2. invoiceDetail Table
**Purpose**: Stores line items for each invoice

**Required Fields**:
- `id` (Primary Key, Auto-increment)
- `invoiceMasterID` (Foreign Key to invoiceMaster)
- `item` (Foreign Key to items/products table)
- `quantity` (Decimal: Quantity of item)
- `price` (Decimal: Unit price)
- `notes` (String: Line item notes)
- `storeID` (Foreign Key to store)
- `discountAmount` (Decimal: Line discount in currency)
- `discountPercentage` (Decimal: Line discount percentage)
- `taxAmount` (Decimal: Line tax in currency)
- `taxPercentage` (Decimal: Line tax percentage)
- `createdBy` (Integer: User ID who created)
- `createdOn` (DateTime: Creation timestamp)
- `updatedBy` (Integer: User ID who last updated)
- `updatedOn` (DateTime: Last update timestamp)
- `deletedBy` (Integer: User ID who deleted)
- `deletedOn` (DateTime: Deletion timestamp)
- `isDeleted` (Boolean: Soft delete flag)

### 3. transactions Table
**Purpose**: Records all accounting transactions for double-entry bookkeeping

**Required Fields**:
- `id` (Primary Key, Auto-increment)
- `invoiceID` (Foreign Key to invoiceMaster)
- `accountID` (Foreign Key to chart of accounts)
- `customerVendorID` (Foreign Key to customer/vendor)
- `amount` (Decimal: Transaction amount - positive for debit, negative for credit)
- `type` (Integer: 1=Receipt, 2=Payment)
- `notes` (String: Transaction description)
- `createdBy` (Integer: User ID who created)
- `createdOn` (DateTime: Creation timestamp)
- `updatedBy` (Integer: User ID who updated)
- `updatedOn` (DateTime: Update timestamp)
- `deletedBy` (Integer: User ID who deleted)
- `deletedOn` (DateTime: Deletion timestamp)
- `isDeleted` (Boolean: Soft delete flag)

## Account IDs Used
- **Cash Account**: 35
- **Visa Account**: 10
- **Vendors Deferred Account**: 38 (for purchase invoices)
- **Customers Deferred Account**: 36 (for sales invoices)

## POST Endpoint Requirements

### Endpoint: `/api/invoices`

### Request Payload Structure
```json
{
  "invoiceMaster": {
    "invoiceType": 1,
    "customerOrVendorID": 123,
    "storeId": 1,
    "paymentType": 1,
    "invoiceGroup": 1,
    "notes": "Invoice notes",
    "discountAmount": 0.00,
    "discountPercentage": 0.00,
    "taxAmount": 15.00,
    "taxPercentage": 15.00,
    "netTotal": 115.00,
    "status": 1,
    "returnStatus": 0,
    "originalInvoiceID": null
  },
  "invoiceDetails": [
    {
      "item": 456,
      "quantity": 2.0,
      "price": 50.00,
      "notes": "Item notes",
      "discountAmount": 0.00,
      "discountPercentage": 0.00,
      "taxAmount": 15.00,
      "taxPercentage": 15.00
    }
  ]
}
```

## Processing Logic

### Step 1: Insert Invoice Master
1. Extract current user ID from authentication context
2. Set `createdBy` to current user ID
3. Set `createdOn` to current timestamp
4. Insert into `invoiceMaster` table
5. Retrieve the generated `invoiceMasterID`

### Step 2: Insert Invoice Details
1. For each item in `invoiceDetails` array:
   - Set `invoiceMasterID` to the ID from Step 1
   - Set `createdBy` to current user ID
   - Set `createdOn` to current timestamp
   - Insert into `invoiceDetail` table

### Step 3: Record Accounting Transactions
Based on `invoiceType` and `paymentType`, create appropriate transaction records:

#### For Purchase Invoice (Type 1):
- **Invoice Transaction**: 
  - `amount` = +netTotal (Debit)
  - `accountID` = payment account (35=Cash, 10=Visa, 38=Vendors for Deferred)
- **Voucher Transaction** (if not deferred):
  - `amount` = -netTotal (Credit)
  - `type` = 2 (Payment)
  - `accountID` = same as invoice transaction

#### For Sales Invoice (Type 2):
- **Invoice Transaction**:
  - `amount` = -netTotal (Credit)
  - `accountID` = payment account (35=Cash, 10=Visa, 36=Customers for Deferred)
- **Voucher Transaction** (if not deferred):
  - `amount` = +netTotal (Debit)
  - `type` = 1 (Receipt)
  - `accountID` = same as invoice transaction

#### For Return Purchase Invoice (Type 3):
- **Invoice Transaction**:
  - `amount` = -netTotal (Credit - opposite of purchase)
  - `accountID` = payment account
- **Voucher Transaction** (if not deferred):
  - `amount` = +netTotal (Debit - opposite of purchase)
  - `type` = 1 (Receipt)
  - `accountID` = same as invoice transaction

#### For Return Sales Invoice (Type 4):
- **Invoice Transaction**:
  - `amount` = +netTotal (Debit - opposite of sales)
  - `accountID` = payment account
- **Voucher Transaction** (if not deferred):
  - `amount` = -netTotal (Credit - opposite of sales)
  - `type` = 2 (Payment)
  - `accountID` = same as invoice transaction

### Step 4: Transaction Fields
For each transaction record:
- Set `invoiceID` to the invoice master ID
- Set `customerVendorID` from request
- Set `createdBy` to current user ID
- Set `createdOn` to current timestamp
- Set `notes` from invoice notes (optional)

## Response Format
```json
{
  "success": true,
  "invoiceId": 12345,
  "message": "Invoice saved successfully"
}
```

## Error Handling
- Validate all required fields
- Ensure customer/vendor exists
- Verify store access permissions
- Validate invoice type values (1-4)
- Validate payment type values (1-3)
- Handle database transaction rollback on any failure
- Return appropriate HTTP status codes and error messages

## Business Rules
1. **Deferred Payments**: When `paymentType = 3`, only create the invoice transaction, not the voucher transaction
2. **Return Invoices**: Must reference `originalInvoiceID` for return types (3, 4)
3. **Soft Deletes**: All deletions set `isDeleted = true` and populate delete metadata
4. **Audit Trail**: All records must track creation and modification metadata
5. **Double Entry**: Every non-deferred invoice creates two offsetting transaction entries
6. **Amount Calculations**: Line totals = (price × quantity - discountAmount + taxAmount)

## Return Invoice System

### Return Status Fields
The system tracks return statuses at both the original invoice level and manages partial/full returns:

#### Original Invoice Return Status (`returnStatus` field):
- `0` = Not Returned (default)
- `1` = Partially Returned (some items/quantities returned)
- `2` = Fully Returned (all items completely returned)

#### Invoice Payment Status (`status` field):
- `0` = Paid
- `1` = Unpaid  
- `2` = Partially Paid

### Return Invoice Processing Logic

#### Step 1: Create Return Invoice
1. **Validate Original Invoice**: Ensure original invoice exists and has available quantities
2. **Calculate Available Quantities**: For each item, calculate remaining quantity available for return
3. **Create Return Invoice Record**:
   - Set `invoiceType` = 3 (Return Purchase) or 4 (Return Sales)
   - Set `originalInvoiceID` = original invoice ID
   - Set same `customerOrVendorID` and `storeId` as original
   - Calculate `netTotal` based on returned quantities and prices

#### Step 2: Update Original Invoice Return Status
After creating a return invoice, automatically update the original invoice's `returnStatus`:

```sql
-- Calculate if invoice is fully or partially returned
-- Compare original quantities vs total returned quantities per item
UPDATE invoiceMaster 
SET returnStatus = CASE
    WHEN all_items_fully_returned THEN 2  -- Fully returned
    WHEN any_items_returned THEN 1        -- Partially returned  
    ELSE 0                                 -- Not returned
END
WHERE id = original_invoice_id;
```

#### Step 3: Available Quantity Calculation
For each item in an invoice, calculate available quantity for returns:

```
Available Quantity = Original Quantity - Total Returned Quantity

WHERE Total Returned Quantity = SUM of quantities from all return invoices 
                               WHERE originalInvoiceID = original_invoice_id 
                               AND item = specific_item_id
                               AND isDeleted = false
```

### Return Invoice Transaction Logic

Return invoices create **opposite** accounting entries compared to original invoices:

#### Return Purchase Invoice (Type 3):
- **Purpose**: Return items to vendor, get money back
- **Invoice Transaction**: `amount = -netTotal` (Credit - opposite of purchase)
- **Voucher Transaction**: `amount = +netTotal` (Debit - opposite of purchase)
- **Voucher Type**: 1 (Receipt - we receive money back)

#### Return Sales Invoice (Type 4):
- **Purpose**: Customer returns items, we pay money back
- **Invoice Transaction**: `amount = +netTotal` (Debit - opposite of sales)
- **Voucher Transaction**: `amount = -netTotal` (Credit - opposite of sales)
- **Voucher Type**: 2 (Payment - we pay money back)

### Return Invoice API Endpoints

#### POST `/api/returns`

**Request Payload**:
```json
{
  "originalInvoiceId": 123,
  "returnType": 3,  // 3=Return Purchase, 4=Return Sales
  "paymentType": 1, // 1=Cash, 2=Visa, 3=Deferred
  "notes": "Return reason",
  "returnDetails": [
    {
      "item": 456,
      "originalQuantity": 10.0,
      "returnQuantity": 3.0,
      "price": 50.00,
      "notes": "Damaged items"
    }
  ]
}
```

**Processing Steps**:
1. **Validate Original Invoice**: Ensure invoice exists and is not deleted
2. **Check Available Quantities**: Verify each item has sufficient available quantity
3. **Create Return Invoice Master**: Insert new invoice with `originalInvoiceID` reference
4. **Create Return Invoice Details**: Insert line items with return quantities
5. **Record Return Transactions**: Create accounting entries (opposite of original)
6. **Update Original Invoice Status**: Recalculate and update `returnStatus`

#### GET `/api/invoices/{id}/available-returns`

**Response**: List of items with available quantities for return
```json
{
  "invoiceId": 123,
  "items": [
    {
      "itemId": 456,
      "originalQuantity": 10.0,
      "totalReturned": 2.0,
      "availableForReturn": 8.0,
      "price": 50.00
    }
  ]
}
```

### Business Rules for Returns

1. **Return Quantity Validation**: Cannot return more than original quantity minus already returned
2. **Price Consistency**: Return items at original invoice prices
3. **Same Customer/Vendor**: Returns must be for same customer/vendor as original
4. **Same Store**: Returns processed in same store as original invoice
5. **Cascade Status Updates**: Original invoice status updates automatically when returns are processed
6. **Return Status Filtering**: Invoices with `returnStatus = 2` (fully returned) excluded from return invoice selection
7. **Soft Delete Impact**: Deleted return invoices should trigger recalculation of original invoice return status

### Remaining Amount Calculations

#### For Payment Status (Deferred Invoices):
```
Remaining Amount = netTotal - totalPaid
Invoice Status = CASE
    WHEN totalPaid >= netTotal THEN 0  -- Paid
    WHEN totalPaid > 0 THEN 2          -- Partially Paid
    ELSE 1                             -- Unpaid
END
```

#### For Return Status (All Invoices):
```
Remaining Returnable Amount = SUM(
    (original_detail.quantity - returned_quantities) * original_detail.price
) FOR each item in original invoice
```

### Transaction Model Explanation

#### Why We Create Transactions for Invoices

The system implements **double-entry bookkeeping** principles where every financial transaction affects at least two accounts. This ensures:

1. **Accounting Accuracy**: Books always balance (total debits = total credits)
2. **Financial Auditing**: Complete trail of all money movements
3. **Business Intelligence**: Track cash flow, receivables, payables
4. **Compliance**: Meet accounting standards and regulations

#### Transaction Types by Invoice Type

**Regular Invoices (Types 1 & 2)**:
- Create TWO transaction records (except for deferred payments)
- One for the invoice amount (asset/liability change)
- One for the payment/receipt (cash/payment account change)

**Return Invoices (Types 3 & 4)**:
- Create OPPOSITE transactions to reverse original accounting impact
- Maintains accounting integrity when items are returned
- Automatically adjusts account balances

#### Transaction Record Structure
Each transaction contains:
- `invoiceID`: Links transaction to specific invoice
- `accountID`: Which account is affected (Cash=35, Visa=10, etc.)
- `customerVendorID`: Who the transaction involves
- `amount`: Positive for debits, negative for credits
- `type`: 1=Receipt (money in), 2=Payment (money out)

#### Example Transaction Flow

**Original Sales Invoice ($100)**:
1. Customer account debited: +$100 (they owe us)
2. Cash account credited: -$100 (we receive cash)

**Return Sales Invoice ($30)**:
1. Customer account credited: -$30 (they owe us less)
2. Cash account debited: +$30 (we pay cash back)

### Data Integrity Rules

1. **Referential Integrity**: Return invoices must reference valid original invoices
2. **Quantity Constraints**: Total returned quantity per item cannot exceed original quantity
3. **Status Consistency**: Original invoice `returnStatus` must reflect actual return state
4. **Transaction Pairing**: Each return invoice should have corresponding accounting transactions
5. **Audit Trail**: All return operations logged with user and timestamp information

## Additional Considerations
- Implement proper database transactions to ensure data consistency
- Add validation for negative quantities in return invoices
- Consider implementing invoice numbering/sequence logic
- Add support for multi-currency if needed
- Implement proper user permission checks based on store access
- Consider adding inventory update logic for item quantities
- Implement background jobs to recalculate return statuses periodically
- Add alerts for return threshold limits per customer/vendor
- Consider return approval workflow for high-value returns
- Add comprehensive logging for all return operations
- Implement return reason codes and categorization
- Consider return time limits (e.g., returns allowed within 30 days)
- Add reporting endpoints for return analytics and trends

## Dummy POST Request Example

### Save Invoice Endpoint
**Endpoint**: `POST /api/invoices/save`

**Request Headers**:
```http
Content-Type: application/json
Authorization: Bearer {user_token}
```

**Request Body Example** (Sales Invoice):
```json
{
  "invoiceType": 2,
  "customerOrVendorID": 15,
  "storeId": 3,
  "status": 1,
  "paymentType": 1,
  "notes": "Sale to customer ABC Company",
  "discountAmount": 50.00,
  "discountPercentage": 5.0,
  "taxAmount": 125.00,
  "taxPercentage": 14.0,
  "netTotal": 2375.00,
  "totalPaid": 2375.00,
  "returnStatus": 0,
  "originalInvoiceID": null,
  "invoiceDetails": [
    {
      "item": 101,
      "quantity": 5.0,
      "price": 200.00,
      "notes": "Premium product batch A"
    },
    {
      "item": 205,
      "quantity": 10.0,
      "price": 150.00,
      "notes": "Standard product batch B"
    }
  ]
}
```

**Response Example** (Success):
```json
{
  "success": true,
  "message": "Invoice saved successfully",
  "data": {
    "invoiceId": 1234,
    "invoiceNumber": "INV-2025-001234",
    "netTotal": 2375.00,
    "status": "Saved",
    "createdAt": "2025-09-18T15:30:00Z"
  }
}
```

**Response Example** (Error):
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": {
    "customerOrVendorID": ["Customer/Vendor not found"],
    "invoiceDetails": ["At least one item is required"],
    "netTotal": ["Net total cannot be negative"]
  }
}
```

**cURL Example**:
```bash
curl -X POST "http://localhost:8000/api/invoices/save" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your_token_here" \
  -d '{
    "invoiceType": 2,
    "customerOrVendorID": 15,
    "storeId": 3,
    "status": 1,
    "paymentType": 1,
    "notes": "Sale to customer ABC Company",
    "discountAmount": 50.00,
    "discountPercentage": 5.0,
    "taxAmount": 125.00,
    "taxPercentage": 14.0,
    "netTotal": 2375.00,
    "totalPaid": 2375.00,
    "returnStatus": 0,
    "originalInvoiceID": null,
    "invoiceDetails": [
      {
        "item": 101,
        "quantity": 5.0,
        "price": 200.00,
        "notes": "Premium product batch A"
      },
      {
        "item": 205,
        "quantity": 10.0,
        "price": 150.00,
        "notes": "Standard product batch B"
      }
    ]
  }'
```