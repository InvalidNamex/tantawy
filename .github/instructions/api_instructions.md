Here we will discuss the API endpoints.
Rule 1: for each endpoint we make there, I want you to include a swagger documentation for it.

## 1. Agent Login API

**URL:** `POST http://127.0.0.1:8000/api/agents/login/`

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "username": "your_username",
  "password": "your_password"
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "agent_id": 1,
  "agent_name": "اسم المندوب",
  "token": "1",
  "storeID": 3
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Invalid credentials"
}
```

**Swagger Documentation:** http://127.0.0.1:8000/api/schema/swagger-ui/

## 2. Agent Sales Invoices API

**URL:** `GET http://127.0.0.1:8000/api/agents/{agent_id}/invoices/`

**Headers:**
```
Content-Type: application/json
```

**Example:** `GET http://127.0.0.1:8000/api/agents/1/invoices/`

**Swagger Documentation:** http://127.0.0.1:8000/api/schema/swagger-ui/

## 3. Save Invoice API

**URL:** `POST http://127.0.0.1:8000/api/invoices/create/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {agent_token}
```

**Authentication:** Requires agent token authentication (use agent ID as token)

**Body:**
```json
{
  "invoiceMaster": {
    "invoiceType": 2,
    "customerOrVendorID": 15,
    "storeId": 3,
    "agentID": 1,
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
    "originalInvoiceID": null
  },
  "invoiceDetails": [
    {
      "item": 101,
      "quantity": 5.0,
      "price": 200.00,
      "notes": "Premium product batch A"
    }
  ]
}
```

**Swagger Documentation:** http://127.0.0.1:8000/api/schema/swagger-ui/

## 4. Batch Save Invoices API

**URL:** `POST http://127.0.0.1:8000/api/invoices/batch-create/`

**Headers:**
```
Content-Type: application/json
Authorization: Bearer {agent_token}
```

**Authentication:** Requires agent token authentication (use agent ID as token)

**Body:**
```json
{
  "invoices": [
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 15,
        "storeId": 3,
        "agentID": 1,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 1000.00,
        "totalPaid": 1000.00
      },
      "invoiceDetails": [
        {
          "item": 101,
          "quantity": 2.0,
          "price": 500.00,
          "notes": "Item batch 1"
        }
      ]
    },
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 20,
        "storeId": 3,
        "agentID": 1,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #2",
        "netTotal": 1500.00,
        "totalPaid": 1500.00
      },
      "invoiceDetails": [
        {
          "item": 205,
          "quantity": 3.0,
          "price": 500.00,
          "notes": "Item batch 2"
        }
      ]
    }
  ]
}
```

**Success Response:**
```json
{
  "success": true,
  "message": "Batch processing completed successfully. 3 invoices created.",
  "data": {
    "total_invoices": 3,
    "total_amount": "5700.00",
    "invoices": [
      {
        "invoice_id": 123,
        "invoice_number": "INV-000123",
        "net_total": "3000.00"
      },
      {
        "invoice_id": 124,
        "invoice_number": "INV-000124", 
        "net_total": "1000.00"
      },
      {
        "invoice_id": 125,
        "invoice_number": "INV-000125",
        "net_total": "1700.00"
      }
    ]
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Authentication required"
}
```

**Swagger Documentation:** http://127.0.0.1:8000/api/schema/swagger-ui/

## 5. Test Examples

Here are working examples with real data:

**Example 1: Single Invoice Batch**
```json
{
  "invoices": [
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 3,
        "storeId": 4,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 3000.00,
        "totalPaid": 3000.00
      },
      "invoiceDetails": [
        {
          "item": 2,
          "quantity": 2.0,
          "price": 500.00,
          "notes": "Item batch 1"
        },
                {
          "item": 3,
          "quantity": 5.0,
          "price": 400.00,
          "notes": "Item batch 1"
        }
      ]
    },
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 2,
        "storeId": 4,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 1000.00,
        "totalPaid": 1000.00
      },
      "invoiceDetails": [
        {
          "item": 1,
          "quantity": 2.0,
          "price": 500.00,
          "notes": "Item batch 1"
        }
      ]
    },
     {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 4,
        "storeId": 4,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 1700.00,
        "totalPaid": 1700.00
      },
      "invoiceDetails": [
        {
          "item": 5,
          "quantity": 1.0,
          "price": 500.00
        },
                {
          "item": 6,
          "quantity": 2.0,
          "price": 300.00
        },
                        {
          "item": 7,
          "quantity": 3.0,
          "price": 200.00
        }
      ]
    }
  ]
}

**URL:** `POST http://127.0.0.1:8000/api/invoices/batch-create/`
Headers: Content-Type: application/json
body: raw json
{
  "invoices": [
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 3,
        "storeId": 4,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 3000.00,
        "totalPaid": 3000.00
      },
      "invoiceDetails": [
        {
          "item": 2,
          "quantity": 2.0,
          "price": 500.00,
          "notes": "Item batch 1"
        },
                {
          "item": 3,
          "quantity": 5.0,
          "price": 400.00,
          "notes": "Item batch 1"
        }
      ]
    },
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 2,
        "storeId": 4,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 1000.00,
        "totalPaid": 1000.00
      },
      "invoiceDetails": [
        {
          "item": 1,
          "quantity": 2.0,
          "price": 500.00,
          "notes": "Item batch 1"
        }
      ]
    },
     {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 4,
        "storeId": 4,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "notes": "Batch invoice #1",
        "netTotal": 1700.00,
        "totalPaid": 1700.00
      },
      "invoiceDetails": [
        {
          "item": 5,
          "quantity": 1.0,
          "price": 500.00
        },
                {
          "item": 6,
          "quantity": 2.0,
          "price": 300.00
        },
                        {
          "item": 7,
          "quantity": 3.0,
          "price": 200.00
        }
      ]
    }
  ]
}