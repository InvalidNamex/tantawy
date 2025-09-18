# Invoice API Documentation for Mobile App

## Overview
This document provides comprehensive API documentation for creating and managing invoices in the Tantawy system. The API supports 4 types of invoices with full transaction processing.

## Base URL
```
http://your-server-domain.com/core/api/
```

## Authentication
All API endpoints require authentication. Include the user authentication token in your requests.

## Invoice Types
- **1**: Purchase Invoice (buying from vendors)
- **2**: Sales Invoice (selling to customers)
- **3**: Return Purchase Invoice (returning items to vendors)
- **4**: Return Sales Invoice (customer returning items)

## Payment Types
- **1**: Cash
- **2**: Visa/Credit Card
- **3**: Deferred/Partial Payment

## Account IDs (for reference)
- **Cash Account**: 35
- **Visa Account**: 10
- **Vendors Deferred Account**: 38
- **Customers Deferred Account**: 36

---

## 1. Create Invoice

### Endpoint
```
POST /api/invoices/
```

### Request Headers
```
Content-Type: application/json
Authorization: Bearer YOUR_TOKEN_HERE
```

### Request Body Structure
```json
{
  "invoiceMaster": {
    "invoiceType": 1,
    "customerOrVendorID": 123,
    "storeId": 1,
    "paymentType": 1,
    "notes": "Invoice notes",
    "discountAmount": 0.00,
    "discountPercentage": 0.00,
    "taxAmount": 15.00,
    "taxPercentage": 15.00,
    "netTotal": 115.00,
    "status": 0,
    "totalPaid": 115.00,
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

### Example Requests

#### 1.1 Purchase Invoice (Cash Payment)
```json
{
  "invoiceMaster": {
    "invoiceType": 1,
    "customerOrVendorID": 101,
    "storeId": 1,
    "paymentType": 1,
    "notes": "Office supplies purchase",
    "discountAmount": 10.00,
    "discountPercentage": 0.00,
    "taxAmount": 20.00,
    "taxPercentage": 15.00,
    "netTotal": 210.00,
    "status": 0,
    "totalPaid": 210.00,
    "returnStatus": 0
  },
  "invoiceDetails": [
    {
      "item": 1,
      "quantity": 5.0,
      "price": 40.00,
      "notes": "Premium pens",
      "discountAmount": 10.00,
      "discountPercentage": 0.00,
      "taxAmount": 20.00,
      "taxPercentage": 15.00
    }
  ]
}
```

#### 1.2 Sales Invoice (Visa Payment)
```json
{
  "invoiceMaster": {
    "invoiceType": 2,
    "customerOrVendorID": 205,
    "storeId": 1,
    "paymentType": 2,
    "notes": "Customer purchase",
    "discountAmount": 0.00,
    "discountPercentage": 10.00,
    "taxAmount": 13.50,
    "taxPercentage": 15.00,
    "netTotal": 103.50,
    "status": 0,
    "totalPaid": 103.50,
    "returnStatus": 0
  },
  "invoiceDetails": [
    {
      "item": 2,
      "quantity": 3.0,
      "price": 30.00,
      "notes": "Notebook set",
      "discountAmount": 0.00,
      "discountPercentage": 10.00,
      "taxAmount": 13.50,
      "taxPercentage": 15.00
    }
  ]
}
```

#### 1.3 Deferred Payment Invoice
```json
{
  "invoiceMaster": {
    "invoiceType": 1,
    "customerOrVendorID": 101,
    "storeId": 1,
    "paymentType": 3,
    "notes": "Bulk order - pay later",
    "discountAmount": 0.00,
    "discountPercentage": 0.00,
    "taxAmount": 0.00,
    "taxPercentage": 0.00,
    "netTotal": 1000.00,
    "status": 1,
    "totalPaid": 0.00,
    "returnStatus": 0
  },
  "invoiceDetails": [
    {
      "item": 3,
      "quantity": 100.0,
      "price": 10.00,
      "notes": "Bulk items",
      "discountAmount": 0.00,
      "discountPercentage": 0.00,
      "taxAmount": 0.00,
      "taxPercentage": 0.00
    }
  ]
}
```

#### 1.4 Return Purchase Invoice
```json
{
  "invoiceMaster": {
    "invoiceType": 3,
    "customerOrVendorID": 101,
    "storeId": 1,
    "paymentType": 1,
    "notes": "Defective items return",
    "discountAmount": 0.00,
    "discountPercentage": 0.00,
    "taxAmount": 3.00,
    "taxPercentage": 15.00,
    "netTotal": 23.00,
    "status": 0,
    "totalPaid": 23.00,
    "returnStatus": 0,
    "originalInvoiceID": 150
  },
  "invoiceDetails": [
    {
      "item": 1,
      "quantity": 1.0,
      "price": 20.00,
      "notes": "Defective pen",
      "discountAmount": 0.00,
      "discountPercentage": 0.00,
      "taxAmount": 3.00,
      "taxPercentage": 15.00
    }
  ]
}
```

### Response Format
```json
{
  "success": true,
  "invoiceId": 12345,
  "message": "Purchase Invoice saved successfully"
}
```

### Error Response
```json
{
  "success": false,
  "message": "Error description here"
}
```

---

## 2. Get Invoices by Type

### Endpoint
```
GET /api/invoices/type/{invoice_type}/
```

### Parameters
- `invoice_type` (required): 1, 2, 3, or 4
- `search` (optional): Search in customer/vendor name, notes, or invoice ID
- `sort_by` (optional): Field to sort by (default: createdAt)
- `sort_order` (optional): 'asc' or 'desc' (default: desc)
- `page` (optional): Page number (default: 1)
- `page_size` (optional): Items per page (default: 20)

### Example Requests

#### 2.1 Get All Purchase Invoices
```
GET /api/invoices/type/1/
```

#### 2.2 Get Sales Invoices with Search
```
GET /api/invoices/type/2/?search=Ahmed&sort_by=netTotal&sort_order=desc&page=1&page_size=10
```

### Response Format
```json
{
  "success": true,
  "invoices": [
    {
      "id": 123,
      "customerOrVendorName": "Ahmed Hassan",
      "storeName": "Main Store",
      "netTotal": 150.75,
      "paymentType": "Cash",
      "status": "Paid",
      "returnStatus": "Not Returned",
      "notes": "Regular customer purchase",
      "createdBy": "user123",
      "createdAt": "2025-09-18T10:30:00Z",
      "updatedAt": "2025-09-18T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_count": 45,
    "total_pages": 3
  }
}
```

---

## 3. Get Invoice Details

### Endpoint
```
GET /api/invoices/{invoice_id}/
```

### Example Request
```
GET /api/invoices/123/
```

### Response Format
```json
{
  "success": true,
  "invoice": {
    "id": 123,
    "invoiceType": 2,
    "invoiceTypeName": "Sales",
    "customerOrVendorID": 205,
    "customerOrVendorName": "Ahmed Hassan",
    "storeID": 1,
    "storeName": "Main Store",
    "paymentType": 1,
    "paymentTypeName": "Cash",
    "status": 0,
    "statusName": "Paid",
    "returnStatus": 0,
    "returnStatusName": "Not Returned",
    "notes": "Customer purchase",
    "discountAmount": 0.00,
    "discountPercentage": 10.00,
    "taxAmount": 13.50,
    "taxPercentage": 15.00,
    "netTotal": 103.50,
    "totalPaid": 103.50,
    "originalInvoiceID": null,
    "createdBy": "user123",
    "createdAt": "2025-09-18T10:30:00Z",
    "updatedAt": "2025-09-18T10:30:00Z"
  },
  "details": [
    {
      "id": 456,
      "itemID": 2,
      "itemName": "Notebook Set",
      "quantity": 3.0,
      "price": 30.00,
      "notes": "Premium notebooks",
      "discountAmount": 0.00,
      "discountPercentage": 10.00,
      "taxAmount": 13.50,
      "taxPercentage": 15.00,
      "lineTotal": 103.50
    }
  ],
  "transactions": [
    {
      "id": 789,
      "accountID": 35,
      "accountName": "Cash Account",
      "amount": -103.50,
      "type": 2,
      "notes": "Sales Invoice #123",
      "createdAt": "2025-09-18T10:30:00Z"
    },
    {
      "id": 790,
      "accountID": 35,
      "accountName": "Cash Account",
      "amount": 103.50,
      "type": 1,
      "notes": "Receipt for Sales Invoice #123",
      "createdAt": "2025-09-18T10:30:00Z"
    }
  ]
}
```

---

## 4. Get Available Items for Return

### Endpoint
```
GET /api/invoices/{invoice_id}/available-returns/
```

### Example Request
```
GET /api/invoices/150/available-returns/
```

### Response Format
```json
{
  "success": true,
  "invoiceId": 150,
  "items": [
    {
      "itemId": 1,
      "itemName": "Premium Pen",
      "originalQuantity": 5.0,
      "totalReturned": 1.0,
      "availableForReturn": 4.0,
      "price": 40.00
    },
    {
      "itemId": 2,
      "itemName": "Notebook",
      "originalQuantity": 3.0,
      "totalReturned": 0.0,
      "availableForReturn": 3.0,
      "price": 30.00
    }
  ]
}
```

---

## Business Logic Summary

### Transaction Creation Rules

#### Purchase Invoice (Type 1)
- **Invoice Transaction**: +netTotal (Debit to payment account)
- **Voucher Transaction** (if not deferred): -netTotal (Credit to payment account)

#### Sales Invoice (Type 2)
- **Invoice Transaction**: -netTotal (Credit to payment account)
- **Voucher Transaction** (if not deferred): +netTotal (Debit to payment account)

#### Return Purchase Invoice (Type 3)
- **Invoice Transaction**: -netTotal (Credit - opposite of purchase)
- **Voucher Transaction** (if not deferred): +netTotal (Debit - we receive money back)

#### Return Sales Invoice (Type 4)
- **Invoice Transaction**: +netTotal (Debit - opposite of sales)
- **Voucher Transaction** (if not deferred): -netTotal (Credit - we pay money back)

### Return Status Updates
When a return invoice is created, the original invoice's `returnStatus` is automatically updated:
- **0**: Not Returned
- **1**: Partially Returned (some items returned)
- **2**: Fully Returned (all items returned)

### Error Handling
The API includes comprehensive validation:
- Required field validation
- Customer/vendor existence check
- Store existence check
- Item existence check
- Return quantity validation
- Original invoice validation for returns

### Status Codes
- **200**: Success (GET requests)
- **201**: Created (POST requests)
- **400**: Bad Request (validation errors)
- **401**: Unauthorized
- **404**: Not Found
- **500**: Internal Server Error

---

## Mobile App Integration Tips

### 1. Authentication
```javascript
// Include authentication token in headers
const headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer ' + userToken
};
```

### 2. Error Handling
```javascript
// Always check the success flag
if (response.data.success) {
  // Handle success
  console.log('Invoice created:', response.data.invoiceId);
} else {
  // Handle error
  console.error('Error:', response.data.message);
}
```

### 3. Return Invoice Creation
```javascript
// First, get available items for return
const availableItems = await getAvailableReturns(originalInvoiceId);

// Then create return invoice with valid quantities
const returnInvoice = {
  invoiceMaster: {
    invoiceType: 3, // or 4 for sales returns
    originalInvoiceID: originalInvoiceId,
    // ... other fields
  },
  invoiceDetails: [
    {
      item: itemId,
      quantity: returnQuantity, // Must be <= availableForReturn
      price: originalPrice,
      // ... other fields
    }
  ]
};
```

### 4. Pagination
```javascript
// Handle pagination for large datasets
let page = 1;
let allInvoices = [];

do {
  const response = await getInvoicesByType(invoiceType, page);
  allInvoices = allInvoices.concat(response.data.invoices);
  page++;
} while (page <= response.data.pagination.total_pages);
```

---

## Testing Examples

### Test Purchase Invoice Creation
```bash
curl -X POST http://your-domain.com/core/api/invoices/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "invoiceMaster": {
      "invoiceType": 1,
      "customerOrVendorID": 1,
      "storeId": 1,
      "paymentType": 1,
      "netTotal": 100.00
    },
    "invoiceDetails": [
      {
        "item": 1,
        "quantity": 2.0,
        "price": 50.00
      }
    ]
  }'
```

### Test Invoice Retrieval
```bash
curl -X GET "http://your-domain.com/core/api/invoices/type/1/?page=1&page_size=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

This comprehensive API provides all the functionality needed for your mobile app to handle invoice operations with proper transaction processing and business logic enforcement.