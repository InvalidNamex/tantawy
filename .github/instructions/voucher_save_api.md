# Voucher Save API - POST Request Documentation

## Overview
This document provides detailed specifications for the POST request to save vouchers (payment receipts and receive receipts) in the custom backend API. It explains each field, how to differentiate between payment and receipt vouchers, and the complete processing logic.

## API Endpoint
```http
POST /api/vouchers
```

## Request Structure

### Complete POST Request Body
```json
{
  // === VOUCHER IDENTIFICATION ===
  "voucherType": "receipt",           // "receipt" or "payment" - Determines voucher direction
  "type": 1,                          // Integer: 1=Receipt (money IN), 2=Payment (money OUT)
  
  // === CUSTOMER/VENDOR INFORMATION ===
  "customerVendorId": 123,            // REQUIRED: ID of customer (receipt) or vendor (payment)
  
  // === FINANCIAL DETAILS ===
  "amount": 1000.00,                  // REQUIRED: Total voucher amount (always positive)
  "paymentMethod": "cash",            // Always "cash" - only cash payments supported
  "accountId": 35,                    // Always 35 (Cash Account)
  
  // === METADATA ===
  "notes": "Customer payment",        // Optional: Voucher description
  "voucherDate": "2024-01-15T10:30:00Z",     // Optional: Defaults to current timestamp
  "storeId": 1,                              // REQUIRED: Store where transaction occurs
  
  // === SYSTEM FIELDS (Auto-populated) ===
  "createdBy": 5,                     // User ID creating the voucher
  "createdOn": "2024-01-15T10:30:00Z" // Timestamp of creation
}
```

## Field Explanations

### Core Identification Fields

#### `voucherType` (String) - REQUIRED
- **Purpose**: Human-readable voucher direction
- **Values**: 
  - `"receipt"` = Money coming IN (from customers)
  - `"payment"` = Money going OUT (to vendors)
- **Usage**: Used for display, reporting, and validation

#### `type` (Integer) - REQUIRED  
- **Purpose**: System code for transaction direction and accounting logic
- **Values**:
  - `1` = Receipt Voucher (Money IN from customers)
  - `2` = Payment Voucher (Money OUT to vendors)
- **Database Impact**: Stored in `transactions.type` field
- **Accounting Logic**: Determines debit/credit direction

### Customer/Vendor Fields

#### `customerVendorId` (Integer) - REQUIRED
- **Purpose**: Links voucher to specific customer or vendor
- **Validation**: 
  - For `type=1` (Receipt): Must be a valid Customer ID
  - For `type=2` (Payment): Must be a valid Vendor ID
- **Database Impact**: Stored in `transactions.customerVendorID`
- **Account Impact**: Updates customer/vendor balance

### Financial Fields

#### `amount` (Decimal) - REQUIRED
- **Purpose**: Total voucher amount in system currency
- **Format**: Always positive value (direction determined by `type`)
- **Processing Logic**:
  - Receipt (`type=1`): Stored as positive value
  - Payment (`type=2`): Stored as negative value
- **Validation**: Must be > 0

#### `paymentMethod` (String) - REQUIRED
- **Purpose**: How the money was paid/received
- **Value**: Always `"cash"` (only cash payments supported)
- **Account Mapping**: Always maps to Account ID 35 (Cash on Hand)

#### `accountId` (Integer) - Always 35
- **Purpose**: Chart of accounts ID for cash transactions
- **Value**: Always 35 (Cash Account)
- **Fixed Mapping**: All vouchers use cash account only

### Invoice Allocation Fields

**Note**: Invoice allocation functionality is not implemented in this version. All vouchers are treated as standalone transactions without specific invoice linking.

### Metadata Fields

#### `notes` (String) - Optional
- **Purpose**: Human-readable description of voucher
- **Max Length**: 500 characters
- **Usage**: Appears on printed vouchers and transaction history

#### `voucherDate` (DateTime) - Optional
- **Purpose**: When the voucher transaction occurred
- **Default**: Current server timestamp
- **Format**: ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)
- **Validation**: Cannot be future date

#### `storeId` (Integer) - REQUIRED
- **Purpose**: Store/location where transaction occurred
- **Validation**: Must be valid, active store
- **Usage**: Multi-location businesses, reporting

## Processing Logic

### Step 1: Request Validation
```javascript
// Validate required fields
if (!customerVendorId || !amount || !type || !storeId) {
  throw "Missing required fields";
}

// Validate voucher type consistency
if (type === 1 && voucherType !== "receipt") {
  throw "Type 1 must be receipt voucher";
}
if (type === 2 && voucherType !== "payment") {
  throw "Type 2 must be payment voucher";
}

// Validate customer/vendor exists and is correct type
const customerVendor = await getCustomerVendor(customerVendorId);
if (type === 1 && customerVendor.type !== "customer") {
  throw "Receipt vouchers require customer";
}
if (type === 2 && customerVendor.type !== "vendor") {
  throw "Payment vouchers require vendor";
}
```

### Step 2: Calculate Transaction Amount
```javascript
// Determine transaction amount based on voucher type
let transactionAmount;
if (type === 1) {
  // Receipt: Money IN (positive)
  transactionAmount = Math.abs(amount);
} else {
  // Payment: Money OUT (negative)  
  transactionAmount = -Math.abs(amount);
}
```

### Step 3: Create Voucher Master Record
```sql
INSERT INTO voucherMaster (
  voucherNumber,    -- Auto-generated (RCV-001, PAY-001)
  voucherType,      -- "receipt" or "payment"
  voucherDate,      -- Request date or current timestamp
  customerVendorId, -- Customer/Vendor ID
  totalAmount,      -- Total voucher amount
  paymentMethod,    -- Always "cash"
  accountId,        -- Always 35 (Cash Account)
  notes,           -- Voucher notes
  storeId,         -- Store ID
  createdBy,       -- Current user ID
  createdOn,       -- Current timestamp
  isDeleted        -- false
) VALUES (?, ?, ?, ?, ?, 'cash', 35, ?, ?, ?, ?, false)
```

### Step 4: Create Accounting Transactions

#### For Receipt Voucher (type=1):
```sql
-- Transaction 1: Debit Cash Account (Money IN)
INSERT INTO transactions (
  accountID = 35,           -- Cash Account
  customerVendorID = NULL,
  amount = +1000.00,        -- Positive (Debit)
  type = 1,                 -- Receipt
  voucherID = voucher_id,
  notes = "Cash received from Customer Name"
)

-- Transaction 2: Credit Customer Account (Reduce customer debt)
INSERT INTO transactions (
  accountID = 36,           -- Customer Accounts Receivable
  customerVendorID = 123,   -- Customer ID
  amount = -1000.00,        -- Negative (Credit)
  type = 1,                 -- Receipt
  voucherID = voucher_id,
  notes = "Payment received from Customer Name"
)
```

#### For Payment Voucher (type=2):
```sql
-- Transaction 1: Debit Vendor Account (Reduce business debt)
INSERT INTO transactions (
  accountID = 37,           -- Vendor Accounts Payable
  customerVendorID = 456,   -- Vendor ID
  amount = +800.00,         -- Positive (Debit)
  type = 2,                 -- Payment
  voucherID = voucher_id,
  notes = "Payment made to Vendor Name"
)

-- Transaction 2: Credit Cash Account (Money OUT)
INSERT INTO transactions (
  accountID = 35,           -- Cash Account
  customerVendorID = NULL,
  amount = -800.00,         -- Negative (Credit)
  type = 2,                 -- Payment
  voucherID = voucher_id,
  notes = "Cash payment to Vendor Name"
)
```

### Step 5: Complete Processing
```javascript
// No invoice allocation processing needed
// Voucher creation is complete after transactions are recorded

// Return success response
return {
  success: true,
  voucherId: voucherId,
  voucherNumber: voucherNumber,
  transactionIds: [transaction1Id, transaction2Id]
};
```

## Differentiation Logic

### How to Identify Receipt vs Payment:

#### Method 1: By `type` field (Recommended)
```javascript
if (request.type === 1) {
  // Receipt Voucher (Money IN from customers)
  accountFlow = "debit_cash_credit_customer";
  expectedEntityType = "customer";
} else if (request.type === 2) {
  // Payment Voucher (Money OUT to vendors)
  accountFlow = "debit_vendor_credit_cash";
  expectedEntityType = "vendor";
}
```

#### Method 2: By `voucherType` field
```javascript
if (request.voucherType === "receipt") {
  // Money coming IN
  transactionType = 1;
} else if (request.voucherType === "payment") {
  // Money going OUT
  transactionType = 2;
}
```

#### Method 3: By customer/vendor type
```javascript
const entity = await getCustomerVendor(request.customerVendorId);
if (entity.type === "customer") {
  // Receipt voucher (money from customer)
  voucherDirection = "receipt";
} else if (entity.type === "vendor") {
  // Payment voucher (money to vendor)
  voucherDirection = "payment";
}
```

## Response Format

### Success Response:
```json
{
  "success": true,
  "voucherId": 12345,
  "voucherNumber": "RCV-001",
  "transactionIds": [67890, 67891],
  "message": "Voucher saved successfully",
  "customerVendorBalance": {
    "previousBalance": 2500.00,
    "currentBalance": 1500.00,
    "balanceChange": -1000.00
  }
}
```

### Error Response:
```json
{
  "success": false,
  "error": "INVALID_CUSTOMER_VENDOR",
  "message": "Customer ID 123 not found or inactive",
  "details": {
    "field": "customerVendorId",
    "value": 123,
    "expectedType": "customer"
  }
}
```

## Validation Rules

### Business Validations:
1. **Customer/Vendor Type Match**: Receipt vouchers require customers, payment vouchers require vendors
2. **Amount Positive**: Voucher amount must be > 0
3. **Cash Only**: Only cash payments are supported
4. **Future Date**: Voucher date cannot be in the future
5. **Store Access**: User must have access to specified store

### Data Validations:
1. **Required Fields**: customerVendorId, amount, type, storeId
2. **Numeric Fields**: amount, customerVendorId, storeId must be valid numbers
3. **Date Format**: voucherDate must be valid ISO 8601 format
4. **String Length**: notes max 500 characters
5. **Payment Method**: Must be "cash"

## Example Requests

### Receipt Voucher (Customer Payment):
```json
{
  "voucherType": "receipt",
  "type": 1,
  "customerVendorId": 123,
  "amount": 1000.00,
  "paymentMethod": "cash",
  "notes": "Customer payment",
  "storeId": 1
}
```

### Payment Voucher (Vendor Payment):
```json
{
  "voucherType": "payment",
  "type": 2,
  "customerVendorId": 456,
  "amount": 800.00,
  "paymentMethod": "cash",
  "notes": "Payment to vendor for supplies",
  "storeId": 1
}
```

### Advance Payment (Customer):
```json
{
  "voucherType": "receipt",
  "type": 1,
  "customerVendorId": 123,
  "amount": 500.00,
  "paymentMethod": "cash",
  "notes": "Advance payment from customer",
  "storeId": 1
}
```

This simplified documentation provides everything needed to implement the voucher saving API in your custom backend with cash-only transactions and without invoice allocation complexity.