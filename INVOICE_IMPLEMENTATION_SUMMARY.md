# Invoice API Implementation Summary

## ✅ What Has Been Implemented

### 1. Core Invoice API (`core/invoice_api.py`)
- **Complete invoice creation system** supporting all 4 invoice types
- **Transaction processing** with proper double-entry bookkeeping
- **Return invoice handling** with original invoice status updates
- **Comprehensive validation** for all input data
- **Error handling** with detailed messages

### 2. API Endpoints Created

#### 2.1 Create Invoice
- **Endpoint**: `POST /core/api/invoices/`
- **Functionality**: Creates any of the 4 invoice types with automatic transaction generation
- **Features**:
  - Validates all required fields
  - Creates invoice master and detail records
  - Generates appropriate accounting transactions
  - Updates return status for return invoices
  - Handles deferred payment logic

#### 2.2 Get Invoices by Type
- **Endpoint**: `GET /core/api/invoices/type/{invoice_type}/`
- **Functionality**: Retrieves filtered list of invoices by type
- **Features**:
  - Search functionality (customer/vendor name, notes, ID)
  - Sorting options (any field, ascending/descending)
  - Pagination support
  - Includes related data (customer/vendor names, store names)

#### 2.3 Get Invoice Details
- **Endpoint**: `GET /core/api/invoices/{invoice_id}/`
- **Functionality**: Retrieves complete invoice information
- **Features**:
  - Invoice master data
  - All line items with calculations
  - Associated transactions
  - Related entity information

#### 2.4 Get Available Returns
- **Endpoint**: `GET /core/api/invoices/{invoice_id}/available-returns/`
- **Functionality**: Shows what items can still be returned from an invoice
- **Features**:
  - Calculates remaining returnable quantities
  - Shows original vs returned quantities
  - Includes pricing information

### 3. Business Logic Implementation

#### 3.1 Transaction Creation Rules
✅ **Purchase Invoice (Type 1)**:
- Invoice Transaction: +netTotal (Debit to payment account)
- Voucher Transaction: -netTotal (Credit to payment account) [if not deferred]

✅ **Sales Invoice (Type 2)**:
- Invoice Transaction: -netTotal (Credit to payment account)
- Voucher Transaction: +netTotal (Debit to payment account) [if not deferred]

✅ **Return Purchase Invoice (Type 3)**:
- Invoice Transaction: -netTotal (Credit - opposite of purchase)
- Voucher Transaction: +netTotal (Debit - receive money back) [if not deferred]

✅ **Return Sales Invoice (Type 4)**:
- Invoice Transaction: +netTotal (Debit - opposite of sales)
- Voucher Transaction: -netTotal (Credit - pay money back) [if not deferred]

#### 3.2 Payment Type Handling
✅ **Cash (Type 1)**: Uses Account ID 35
✅ **Visa (Type 2)**: Uses Account ID 10
✅ **Deferred (Type 3)**: Uses Account ID 38 (Vendors) or 36 (Customers)

#### 3.3 Return Status Management
✅ **Automatic Updates**: Original invoice status updates when returns are processed
✅ **Quantity Tracking**: Tracks partial vs full returns per item
✅ **Status Values**: 0=Not Returned, 1=Partially Returned, 2=Fully Returned

### 4. Data Validation & Security

#### 4.1 Input Validation
✅ **Required Fields**: All mandatory fields validated
✅ **Data Types**: Proper decimal/integer validation
✅ **Business Rules**: Invoice type, payment type, status validations
✅ **Foreign Key Validation**: Customer/vendor, store, item existence checks

#### 4.2 Return Invoice Validation
✅ **Original Invoice**: Must exist and be valid
✅ **Type Matching**: Return type must match original (purchase returns for purchases, etc.)
✅ **Quantity Limits**: Cannot return more than originally purchased
✅ **Item Validation**: Items must exist in original invoice

#### 4.3 Security Features
✅ **Authentication Required**: All endpoints require user authentication
✅ **Soft Deletes**: Respects isDeleted flags throughout
✅ **Audit Trail**: CreatedBy, updatedBy tracking
✅ **Transaction Integrity**: Database transactions ensure data consistency

### 5. Mobile App Integration

#### 5.1 Request/Response Format
✅ **JSON API**: Clean JSON request/response format
✅ **Error Handling**: Consistent error response structure
✅ **Success Indicators**: Clear success/failure flags
✅ **Detailed Messages**: Descriptive error and success messages

#### 5.2 Pagination & Search
✅ **Pagination**: Page-based pagination for large datasets
✅ **Search**: Text search across customer/vendor names and notes
✅ **Sorting**: Flexible sorting by any field
✅ **Filtering**: Filter by invoice type

### 6. Documentation & Testing

#### 6.1 API Documentation
✅ **Complete Documentation**: `invoice_api_documentation.md`
✅ **Request Examples**: Sample requests for all invoice types
✅ **Response Examples**: Expected response formats
✅ **Error Scenarios**: Common error cases and responses
✅ **Business Logic**: Detailed explanation of transaction rules

#### 6.2 Test Framework
✅ **Test Script**: `test_invoice_api.py` for API testing
✅ **Sample Data**: Example requests for all scenarios
✅ **Error Testing**: Validation error scenarios

## 🚀 Ready for Mobile App Integration

### URLs Configured
- `POST /core/api/invoices/` - Create invoices
- `GET /core/api/invoices/type/{type}/` - List invoices by type
- `GET /core/api/invoices/{id}/` - Get invoice details
- `GET /core/api/invoices/{id}/available-returns/` - Get returnable items

### Authentication
- All endpoints require user authentication
- Standard Django authentication system

### Database
- All required models already exist in `core/models.py`
- Migrations applied for all invoice tables
- Transaction processing fully implemented

## 📱 Next Steps for Mobile App

1. **Authentication Setup**: Implement token-based auth in mobile app
2. **Test API Calls**: Use provided test script or documentation examples
3. **Error Handling**: Implement proper error handling based on API responses
4. **UI Integration**: Connect mobile UI to the API endpoints
5. **Data Sync**: Implement data synchronization for offline capability

## 🔍 API Features Summary

| Feature | Status | Description |
|---------|---------|-------------|
| Invoice Creation | ✅ Complete | All 4 types with transaction processing |
| Return Processing | ✅ Complete | Automatic status updates and validation |
| Transaction Accounting | ✅ Complete | Double-entry bookkeeping implementation |
| Data Validation | ✅ Complete | Comprehensive input validation |
| Search & Pagination | ✅ Complete | Flexible querying capabilities |
| Error Handling | ✅ Complete | Detailed error messages and codes |
| Documentation | ✅ Complete | Full API documentation with examples |
| Authentication | ✅ Complete | Secure endpoint access |

The invoice API is now **production-ready** and fully implements the business logic specified in your `invoice.md` documentation. Your mobile app can immediately start using these endpoints to create and manage all types of invoices with proper accounting transactions.

New Point:
# Invoice System Logic Documentation

## Executive Summary

### Overview
This document provides implementation guidelines for a custom backend API to handle a complete invoice management system with double-entry accounting principles.

### Core Components

#### **Invoice Types (4 Types)**
- **Purchase (1)**: Buy from vendors
- **Sales (2)**: Sell to customers  
- **Return Purchase (3)**: Return items to vendors
- **Return Sales (4)**: Accept returns from customers

#### **Database Structure (3 Main Tables)**
1. **invoiceMaster**: Header information (totals, customer/vendor, payment type)
2. **invoiceDetail**: Line items (products, quantities, prices)
3. **transactions**: Accounting entries for double-entry bookkeeping

#### **Payment Methods**
- **Cash (35)**: Immediate cash payment
- **Visa (10)**: Card/bank payment
- **Deferred (36/38)**: Credit payment (customers=36, vendors=38)

### Key Features

#### **Invoice Processing**
- Creates invoice master + details
- Generates automatic accounting transactions
- Supports discounts and taxes at line and header level
- Tracks creation/modification audit trail

#### **Return System**
- **Partial Returns**: Some quantities returned (`returnStatus = 1`)
- **Full Returns**: All items returned (`returnStatus = 2`)
- **Available Quantity**: Original - Total Returned per item
- **Automatic Status Updates**: Original invoice status updates when returns processed

#### **Accounting Integration**
- **Double-Entry Bookkeeping**: Every invoice creates offsetting debit/credit entries
- **Account Mapping**: Cash (35), Visa (10), Customer Receivables (36), Vendor Payables (37)
- **Return Transactions**: Create opposite entries to reverse original impact

### Business Logic

#### **Transaction Flow Examples**
- **Sales Invoice**: Debit Customer Account → Credit Cash/Revenue
- **Purchase Invoice**: Debit Inventory → Credit Vendor Account/Cash
- **Return Sales**: Credit Customer Account → Debit Cash (opposite of sales)
- **Return Purchase**: Debit Cash → Credit Vendor Account (opposite of purchase)

#### **Balance Calculations**
- **Customer Balance**: Sum of debits - credits in customer receivable account
- **Vendor Balance**: Sum of credits - debits in vendor payable account
- **Payment Status**: Based on totalPaid vs netTotal
- **Return Status**: Based on returned quantities vs original quantities

### API Structure

#### **Main Endpoint**: `POST /api/invoices`
**Payload**: JSON with invoiceMaster + invoiceDetails array
**Response**: Success with generated invoice ID

#### **Return Endpoints**:
- `POST /api/returns` - Create return invoice
- `GET /api/invoices/{id}/available-returns` - Get returnable items

### Critical Business Rules

1. **Return Validation**: Cannot return more than available quantity
2. **Status Tracking**: Automatic cascade updates for return status
3. **Audit Trail**: Complete tracking of who/when created/modified/deleted
4. **Soft Deletes**: All records use isDeleted flag
5. **Transaction Integrity**: Every non-deferred invoice creates balanced accounting entries
6. **Price Consistency**: Returns use original invoice prices

### Data Integrity
- Referential integrity between tables
- Quantity constraints on returns
- Double-entry balance validation
- Comprehensive audit logging
- User permission validation

This system provides a complete invoice management solution with proper accounting principles, return handling, and financial tracking suitable for business operations.

---

## Detailed Implementation Guide

## Overview
This document provides comprehensive business logic for implementing invoice operations. The system supports four types of invoices with different accounting behaviors and transaction patterns.

## Invoice Types
1. **Purchase Invoice** (Type: 1) - Recording purchases from vendors
2. **Sales Invoice** (Type: 2) - Recording sales to customers  
3. **Return Purchase Invoice** (Type: 3) - Recording returns to vendors
4. **Return Sales Invoice** (Type: 4) - Recording returns from customers

## Data Structure Concepts

### 1. Invoice Master Entity
**Purpose**: Stores the main invoice header information

**Key Concepts**:
- Invoice identification and type classification
- Customer/vendor relationship linking
- Payment method and status tracking
- Financial totals (discounts, taxes, net amounts)
- Return status and original invoice references
- Complete audit trail (created, updated, deleted tracking)
- Soft delete functionality

### 2. Invoice Detail Entity
**Purpose**: Stores line items for each invoice

**Key Concepts**:
- Line item product/service references
- Quantity and pricing information
- Line-level discounts and taxes
- Individual item notes and specifications
- Audit trail for each line item
- Soft delete capability

### 3. Transaction Entity
**Purpose**: Records all accounting transactions for double-entry bookkeeping

**Key Concepts**:
- Account classification and mapping
- Customer/vendor transaction linking
- Debit/credit amount tracking (positive/negative values)
- Transaction type classification
- Invoice relationship for traceability
- Complete audit and deletion tracking

## Account IDs Used
- **Cash Account**: 35
- **Visa Account**: 10
- **Vendors Deferred Account**: 38 (for purchase invoices)
- **Customers Deferred Account**: 36 (for sales invoices)

## API Endpoint Concepts

### Main Invoice Endpoint Logic

### Request Structure Concept
The invoice creation should accept:
- **Invoice Header**: Contains total amounts, customer/vendor info, payment method, and metadata
- **Invoice Details Array**: Contains line items with products, quantities, prices, and line-level calculations
- **System Fields**: User identification, timestamps, and audit information

### Expected Data Elements
- Invoice type classification (purchase/sales/returns)
- Customer or vendor identification
- Store/location context
- Payment method specification
- Financial calculations (discounts, taxes, totals)
- Line item specifications
- Return status and original invoice linking
- Complete audit trail information

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

## Response Concepts
The system should return:
- **Success Indicators**: Clear success/failure status
- **Generated Identifiers**: New invoice ID or transaction references
- **Confirmation Messages**: User-friendly success/error messages
- **Additional Context**: Any relevant business information or warnings

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
After creating a return invoice, automatically update the original invoice's return status:

**Logic**: Calculate return status by comparing original quantities vs total returned quantities per item:
- **Fully Returned (2)**: All items completely returned
- **Partially Returned (1)**: Some items or quantities returned  
- **Not Returned (0)**: No returns processed

**Implementation**: Update original invoice status based on aggregate return analysis

#### Step 3: Available Quantity Calculation
For each item in an invoice, calculate available quantity for returns:

**Formula**: Available Quantity = Original Quantity - Total Returned Quantity

**Logic**: 
- Sum all returned quantities for each specific item from all return invoices
- Link returns to original invoice through reference relationship
- Exclude soft-deleted return records
- Calculate remaining available quantity per item

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

#### Return Invoice Endpoint Logic

**Request Concept**:
The return invoice creation should handle:
- **Original Invoice Reference**: Link to the invoice being returned
- **Return Type Classification**: Purchase return vs sales return
- **Payment Method**: How the return will be processed
- **Return Details**: Items being returned with quantities and pricing
- **Business Logic**: Automatic validation and status updates

**Processing Steps**:
1. **Validate Original Invoice**: Ensure invoice exists and is not deleted
2. **Check Available Quantities**: Verify each item has sufficient available quantity
3. **Create Return Invoice Master**: Insert new invoice with `originalInvoiceID` reference
4. **Create Return Invoice Details**: Insert line items with return quantities
5. **Record Return Transactions**: Create accounting entries (opposite of original)
6. **Update Original Invoice Status**: Recalculate and update `returnStatus`

#### Available Returns Query Logic

**Response Concept**: The system should provide:
- **Invoice Identification**: Reference to the original invoice
- **Item Analysis**: For each item, calculate available return quantities
- **Quantity Tracking**: Original quantity minus total already returned
- **Pricing Information**: Original prices for return processing
- **Business Validation**: Ensure return limits are respected

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
