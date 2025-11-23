# Mobile API Documentation

Quick reference for mobile app development with agent-specific endpoints.

---

## 🔐 Authentication

### Authentication Methods

Your API uses **HTTP Basic Authentication** for all mobile agent endpoints. There is NO token-based authentication currently implemented.

### Timezone Support

**Optional:** Send user's timezone in the `X-Timezone` header for automatic datetime conversion.

**Example Headers:**
```
Authorization: Basic {credentials}
X-Timezone: Africa/Cairo
```

**Supported Timezone Format:** IANA timezone database names (e.g., `Africa/Cairo`, `America/New_York`, `Europe/London`, `Asia/Dubai`)

**How it works:**
- If you send a datetime like `"2025-11-15T14:30:00"` without timezone info, the API will interpret it as being in the timezone specified in the `X-Timezone` header
- If no `X-Timezone` header is provided, the server's default timezone (`Africa/Cairo`) is used
- If you send a datetime with timezone info (e.g., `"2025-11-15T14:30:00Z"`), that timezone is respected

### Agent Login
**POST** `/api/agents/login/`  
**Auth:** None (Public endpoint)

Use this endpoint to verify agent credentials and get agent information. The response includes agent details but does NOT return a usable token.

```json
// Request
{"username": "agent_username", "password": "agent_password"}

// Response
{"success": true, "id": 7, "name": "Agent Name", "token": "agent_token", "storeID": 3}
```

> ⚠️ **Note:** The `token` field in the response is currently just the agent ID. For actual authentication, you must use Basic Auth (username:password) with each request.

### How to Authenticate

**All protected endpoints require HTTP Basic Authentication:**

1. Encode agent credentials: `base64(username:password)`
2. Send in Authorization header: `Authorization: Basic {encoded_credentials}`

**Example (Python):**
```python
import base64
import requests

username = "agent_username"
password = "agent_password"
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "X-Timezone": "Africa/Cairo"  # Optional: User's timezone
}
response = requests.get("https://api.example.com/api/agents/visit-plans/active-with-customers/", headers=headers)
```

**Example (JavaScript):**
```javascript
const username = "agent_username";
const password = "agent_password";
const credentials = btoa(`${username}:${password}`);

// Get user's timezone automatically
const userTimezone = Intl.DateTimeFormat().resolvedOptions().timeZone;

fetch("https://api.example.com/api/agents/visit-plans/active-with-customers/", {
  headers: {
    "Authorization": `Basic ${credentials}`,
    "X-Timezone": userTimezone  // Optional: Automatically detected timezone
  }
})
```

---

## 📋 Visit Plans

### Get Active Visit Plan with Customers
**GET** `/api/agents/visit-plans/active-with-customers/`  
**Auth:** Basic Auth

Returns today's active plan with customer list including price lists.

```json
// Response
{
  "success": true,
  "data": {
    "plan_id": 1,
    "date_from": "2025-10-23",
    "date_to": "2025-10-31",
    "customers": [
      {
        "id": 175,
        "customer_name": "Customer Name",
        "phone_one": "01234567890",
        "price_list": {"id": 3, "name": "Wholesale Price List"}
      }
    ],
    "total_customers": 1
  }
}
```

---

## 📊 GET Endpoints

### Get Sales Invoices
**GET** `/api/agents/invoices/?agent_id=7&invoice_type=2`  
**Auth:** None (Public endpoint - filters by agent_id parameter)

**Parameters:** `agent_id` (required), `invoice_type` (2=Sales, 4=Return), `date_from`, `date_to`, `customer_vendor`

### Get Receive Vouchers
**GET** `/api/agents/transactions/?agent_id=7&transaction_type=1`  
**Auth:** None (Public endpoint - filters by agent_id parameter)

**Parameters:** `agent_id` (required), `transaction_type` (1=Receipt, 2=Payment), `date_from`, `date_to`

### Get Negative Visits
**GET** `/api/visits/negative/?agent_id=7`  
**Auth:** None (Public endpoint - filters by agent_id parameter)

**Parameters:** `agent_id` (required), `date_from`, `date_to`, `customer_vendor`

Returns visits with no related invoices or transactions.

### Get Items (for Invoice Creation)
**GET** `/api/items/`  
**Auth:** None (Public endpoint)

Returns all items with details needed for invoice creation.

```json
// Response
[
  {
    "id": 101,
    "itemName": "Product A",
    "itemGroupId": 5,
    "barcode": "123456",
    "sign": "PC"
  }
]
```

### Get Price List Details
**GET** `/api/price-list-details/pricelist/{pricelist_id}/`  
**Auth:** None (Public endpoint)

Returns items with prices for a specific price list.

```json
// Response
[
  {
    "id": 1,
    "item": {"id": 101, "itemName": "Product A"},
    "priceList": {"id": 3, "priceListName": "Wholesale"},
    "price": 200.00
  }
]
```

### Get Customers List
**GET** `/api/customers/`  
**Auth:** None (Public endpoint)

Returns all active customers for dropdown/selection purposes.

```json
// Response
{
  "success": true,
  "data": [
    {"id": 175, "customerVendorName": "Customer Name"}
  ]
}
```

---

## 📤 POST Endpoints - Bulk Operations

### Bulk Create Sales Invoices
**POST** `/api/invoices/batch-create/`  
**Auth:** Basic Auth (username:password) OR Django Session (for web users)

Accepts either HTTP Basic Authentication with agent credentials OR Django session authentication for web users.

```json
{
  "invoices": [
    {
      "invoiceMaster": {
        "invoiceType": 2,
        "customerOrVendorID": 15,
        "storeId": 3,
        "agentID": 7,
        "status": 1,
        "paymentType": 1,
        "netTotal": 1000.00,
        "totalPaid": 1000.00
      },
      "invoiceDetails": [
        {"item": 101, "quantity": 5.0, "price": 200.00}
      ]
    }
  ]
}
```

**Invoice Types:** 2=Sales, 4=Return Sales  
**Payment Types:** 1=Cash, 2=Visa, 3=Deferred  
**Status:** 0=Paid, 1=Unpaid, 2=Partially Paid

### Bulk Create Vouchers
**POST** `/api/vouchers/batch-create/`  
**Auth:** Basic Auth (username:password)

```json
{
  "vouchers": [
    {
      "type": 1,
      "customerVendorId": 15,
      "amount": 500.00,
      "storeId": 3,
      "notes": "Payment received from customer",
      "voucherDate": "2025-10-23T14:30:00Z",
      "accountId": 35
    },
    {
      "type": 2,
      "amount": 150.00,
      "storeId": 3,
      "notes": "Electricity bill payment",
      "voucherDate": "2025-10-23T15:00:00Z",
      "accountId": 35
    }
  ]
}
```

**Types:** 1=Receipt (IN), 2=Payment (OUT)  
**Required Fields:** `type`, `amount`, `storeId`  
**Optional Fields:** `customerVendorId` (for customer/vendor transactions), `notes`, `voucherDate`, `accountId` (defaults to 35 - Store Cash)  
**Max:** 100 vouchers per batch  
**Voucher ID Format:** `{agent_id}000{r|p}{sequence}`  
**Note:** `customerVendorId` is optional - use it for customer receipts or vendor payments. Omit it for general expenses (utilities, salaries, etc.)

### Bulk Create Visits
**POST** `/api/visits/batch-create/`  
**Auth:** Basic Auth (username:password)

```json
{
  "visits": [
    {
      "transType": 1,
      "customerVendor": 15,
      "date": "2025-10-23T10:30:00Z",
      "latitude": 30.0444,
      "longitude": 31.2357,
      "notes": "Customer not available"
    }
  ]
}
```

**Transaction Types:** 1=Sales, 2=Return Sales, 3=Receive Voucher, 4=Pay Voucher  
**Max:** 100 visits per batch

---

## 🔑 Authentication Details

### Authentication Summary

| Endpoint Type | Authentication Method | Details |
|--------------|----------------------|---------|
| Agent Login | None | Public endpoint for credential verification |
| GET Endpoints (Read-only) | None | Public endpoints with agent_id filtering |
| POST Endpoints (Bulk Operations) | Basic Auth | HTTP Basic Authentication required |
| Visit Plans (Active) | Basic Auth | HTTP Basic Authentication required |

### Basic Auth Implementation

**Header Format:**
```
Authorization: Basic {base64_encoded_credentials}
```

**Python Example:**
```python
import base64
import requests

# Agent credentials
username = "agent_username"
password = "agent_password"

# Encode credentials
credentials = base64.b64encode(f"{username}:{password}".encode()).decode()

# Make authenticated request
headers = {"Authorization": f"Basic {credentials}"}
response = requests.post(
    "https://api.example.com/api/invoices/batch-create/",
    headers=headers,
    json={"invoices": [...]}
)
```

**JavaScript Example:**
```javascript
// Agent credentials
const username = "agent_username";
const password = "agent_password";

// Encode credentials
const credentials = btoa(`${username}:${password}`);

// Make authenticated request
fetch("https://api.example.com/api/invoices/batch-create/", {
  method: "POST",
  headers: {
    "Authorization": `Basic ${credentials}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({invoices: [...]})
});
```

**Flutter/Dart Example:**
```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

// Agent credentials
String username = "agent_username";
String password = "agent_password";

// Encode credentials
String credentials = base64Encode(utf8.encode('$username:$password'));

// Make authenticated request
final response = await http.post(
  Uri.parse('https://api.example.com/api/invoices/batch-create/'),
  headers: {
    'Authorization': 'Basic $credentials',
    'Content-Type': 'application/json',
  },
  body: jsonEncode({'invoices': [...]}),
);
```

### Security Notes

⚠️ **Important Security Considerations:**

1. **Always use HTTPS** - Basic Auth sends credentials with every request, so HTTPS is mandatory
2. **Store credentials securely** - Never hardcode credentials in your app
3. **Session management** - Basic Auth is stateless; credentials are sent with each request
4. **Error handling** - 401 Unauthorized means credentials are invalid or agent is inactive

### Recommended Mobile App Flow

```
1. User Login
   ↓
2. Call /api/agents/login/ with username/password
   ↓
3. If successful, store credentials securely (Keychain/Keystore)
   ↓
4. For all subsequent requests:
   - Encode username:password to Base64
   - Add Authorization: Basic {credentials} header
   ↓
5. On 401 error, prompt user to login again
```

---

## 📝 Implementation Status

| Endpoint | Auth Required | Method | URL |
|----------|---------------|--------|-----|
| Agent Login | ❌ No | POST | `/api/agents/login/` |
| Get Active Visit Plan | ✅ Basic Auth | GET | `/api/agents/visit-plans/active-with-customers/` |
| Get Sales Invoices | ❌ No | GET | `/api/agents/invoices/?agent_id={id}` |
| Get Receive Vouchers | ❌ No | GET | `/api/agents/transactions/?agent_id={id}` |
| Get Negative Visits | ❌ No | GET | `/api/visits/negative/?agent_id={id}` |
| Get Items | ❌ No | GET | `/api/items/` |
| Get Customers | ❌ No | GET | `/api/customers/` |
| Get Price List Details | ❌ No | GET | `/api/price-list-details/pricelist/{id}/` |
| Bulk Create Invoices | ✅ Basic Auth | POST | `/api/invoices/batch-create/` |
| Bulk Create Vouchers | ✅ Basic Auth | POST | `/api/vouchers/batch-create/` |
| Bulk Create Visits | ✅ Basic Auth | POST | `/api/visits/batch-create/` |

**Legend:**
- ✅ = Authentication Required (HTTP Basic Auth)
- ❌ = No Authentication Required (Public endpoint)

---

## 🚀 Key Features

### Authentication Architecture
- **Public GET endpoints** - No authentication required for read operations (filtered by agent_id parameter)
- **Protected POST endpoints** - HTTP Basic Auth required for all write operations
- **Hybrid support** - Batch invoice creation accepts both Basic Auth (mobile) and Django session (web)
- **Security** - All protected endpoints validate agent credentials on each request

### Negative Visits
- Dynamically filters visits with no related invoices/transactions
- No schema changes required
- Flexible date range filtering

### Bulk Operations
- Atomic transactions (all or nothing)
- Maximum 100 items per batch
- Automatic ID generation for vouchers
- Double-entry accounting for vouchers

---

## ⚠️ Important Notes for Frontend Developers

### 1. Authentication Types
- **Read-only operations (GET)**: No authentication needed, use `agent_id` parameter
- **Write operations (POST)**: HTTP Basic Auth required

### 2. Error Responses
```json
// 401 Unauthorized (Invalid credentials or inactive agent)
{"success": false, "message": "Authentication required"}

// 400 Bad Request (Validation error)
{"success": false, "message": "Validation failed", "errors": ["..."]}

// 500 Internal Server Error
{"success": false, "message": "Error message"}
```

### 3. Date Format & Timezone
All dates should be in ISO 8601 format: `2025-10-23T14:30:00Z` or `2025-10-23T14:30:00`

**Timezone Handling:**
- Send the `X-Timezone` header with the user's timezone (IANA format)
- If datetime has no timezone info, it will be interpreted in the user's timezone
- If no `X-Timezone` header is sent, server's default timezone (Africa/Cairo) is used

**Mobile Client Examples:**

**Flutter/Dart:**
```dart
import 'package:timezone/timezone.dart' as tz;

// Get device timezone
String userTimezone = DateTime.now().timeZoneName; // e.g., "Africa/Cairo"

// Add to request headers
final headers = {
  'Authorization': 'Basic $credentials',
  'X-Timezone': userTimezone,
};
```

**React Native:**
```javascript
import { Platform } from 'react-native';
import * as Localization from 'expo-localization';

// Get device timezone
const userTimezone = Localization.timezone; // e.g., "Africa/Cairo"

// Add to request headers
const headers = {
  'Authorization': `Basic ${credentials}`,
  'X-Timezone': userTimezone,
};
```

**Android (Kotlin):**
```kotlin
import java.util.TimeZone

// Get device timezone
val userTimezone = TimeZone.getDefault().id // e.g., "Africa/Cairo"

// Add to request headers
val headers = mapOf(
    "Authorization" to "Basic $credentials",
    "X-Timezone" to userTimezone
)
```

**iOS (Swift):**
```swift
import Foundation

// Get device timezone
let userTimezone = TimeZone.current.identifier // e.g., "Africa/Cairo"

// Add to request headers
let headers = [
    "Authorization": "Basic \(credentials)",
    "X-Timezone": userTimezone
]
```

### 4. Agent Status
Agents must be `isActive=True` and `isDeleted=False` to authenticate

---

**Version:** 3.0  
**Last Updated:** 2025-11-09  
**Status:** Production Ready  
**Authentication:** HTTP Basic Auth (username:password)
