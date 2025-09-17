# Django REST Framework Project Instructions

## Project Overview
I want you to use the project in folder backend for reference.
I will provide you with tables schema and I want you to create models, serializers, views, urls, documentation, swagger, for my DRF project.

## ⚠️ IMPORTANT REQUIREMENT
**One criteria that will always accompany us is that each table will include these audit fields:**
- `createdAt` (DateTime)
- `updatedAt` (DateTime) 
- `deletedAt` (DateTime, nullable)
- `createdBy` (Foreign Key to User)
- `updatedBy` (Foreign Key to User)
- `deletedBy` (Foreign Key to User, nullable)
- `isDeleted` (Boolean)

## 📋 Database Schema Specifications

### 1️⃣ ItemsGroups Table
**Table Name:** `itemsGroups`
- id (Primary Key, Auto-increment)
- itemsGroupName (String, max length 255)

### 2️⃣ Items Table  
**Table Name:** `items`
- id (Primary Key, Auto-increment)
- itemGroupId (Foreign Key to itemsGroups table)
- itemName (String, max length 255)
- itemImage (String, max length 255)
- barcode (String, max length 255)
- sign (String, max length 255)
- isUsed (Boolean)
- isTax (Boolean)
- mainUnitName (String, max length 255)
- subUnitName (String, max length 255)
- subUnitName (String, max length 255)
- mainUnitPack (Decimal)
- subUnitPack (Decimal)
- subUnitBarCode (String, max length 255)
- smallUnitBarCode (String, max length 255)

### 3️⃣ PriceLists Table
**Table Name:** `priceLists`
- id (Primary Key, Auto-increment)
- priceListName (String, max length 255)

### 4️⃣ PriceListsDetails Table
**Table Name:** `priceListsDetails`
- id (Primary Key, Auto-increment)
- priceList (Foreign Key to priceLists table)
- item (Foreign Key to items table)
- price (Decimal)

### 5️⃣ Stores Table
**Table Name:** `stores`
- id (Primary Key, Auto-increment)
- storeName (String, max length 255)
- storeGroup (String, max length 255)

### 6️⃣ StoreGroups Table
**Table Name:** `storeGroups`
- id (Primary Key, Auto-increment)
- storeGroupName (String, max length 255)

---

## 🔧 Implementation Status

### ✅ Completed Changes
- [x] **Instructions formatting**: Added clear markdown structure with emojis and sections
- [x] **Audit fields requirement**: Emphasized the mandatory audit fields for all tables
- [x] **Table numbering**: Added numbered sections for better organization
- [x] **Table names specification**: Explicitly defined table names for each schema
- [x] **Django models created**: All 6 tables implemented with BaseModel for audit fields
- [x] **Database migrations**: Initial migration created and applied (0001_initial)
- [x] **DRF serializers**: Complete serializers for all models with audit fields
- [x] **API views implemented**: Function-based views with proper CRUD operations
- [x] **URL routing configured**: All endpoints properly configured with RESTful patterns
- [x] **Swagger documentation**: drf-spectacular integrated with auto-generated schemas
- [x] **Authentication system**: Complete login/logout with dashboard as index page
- [x] **Beautiful UI**: Modern gradient design with Bootstrap 5 and responsive layout
- [x] **Django models created**: All 6 tables implemented with BaseModel for audit fields
- [x] **Database migrations**: Initial migration created and applied (0001_initial)
- [x] **DRF serializers**: Complete serializers for all models with audit fields
- [x] **API views implemented**: Function-based views with proper CRUD operations
- [x] **URL routing configured**: All endpoints properly configured with RESTful patterns
- [x] **Swagger documentation**: drf-spectacular integrated with auto-generated schemas
- [x] **Invoice system implemented**: Complete CustomerVendor, InvoiceMaster, and InvoiceDetail models
- [x] **Stock management**: Real-time stock calculation based on invoice transactions
- [x] **Admin interfaces**: All models properly registered with comprehensive admin interfaces
- [x] **Documentation**: Comprehensive docstrings and comments throughout codebase
- [x] **Constants**: Centralized constants file for choice fields and maintainability
- [x] **Code organization**: Proper separation of concerns with inlines and structured admin

### 📝 Additional Notes
* **Authentication**: Users will be able to login to admin dashboard and have permissions based on their roles and role group (will be implemented later).
* **File naming**: Follow Django naming conventions for models, serializers, views, and URLs
* **Documentation**: Each implementation should include proper docstrings and comments ✅ **COMPLETED**
* **Swagger**: API documentation should be auto-generated with proper schemas

---

## 🚀 Next Steps
~~1. Create Django models based on the schemas above~~ ✅ **COMPLETED**
~~2. Generate and apply database migrations~~ ✅ **COMPLETED**
~~3. Create DRF serializers for API endpoints~~ ✅ **COMPLETED**
~~4. Implement API views with proper CRUD operations~~ ✅ **COMPLETED**
~~5. Configure URL routing~~ ✅ **COMPLETED**
~~6. Add Swagger documentation~~ ✅ **COMPLETED**
~~7. Implement invoice system with CustomerVendor, InvoiceMaster, InvoiceDetail~~ ✅ **COMPLETED**
~~8. Add stock calculation functionality~~ ✅ **COMPLETED**
9. Test all functionality ⏳ **PENDING** - Only basic test structure exists

### 🎯 Current Implementation Summary:
- **Models**: All 9 tables implemented with proper audit fields (original 6 + 3 invoice tables)
- **Migrations**: All migrations created and applied (0001_initial, 0002_add_invoice_models)
- **Serializers**: Complete DRF serializers for all models including nested relationships
- **Views**: Function-based views with drf-spectacular documentation for all endpoints
- **URLs**: RESTful endpoint routing configured for all models
- **Swagger**: Auto-generated API documentation available at `/api/schema/swagger-ui/`
- **Authentication**: Complete login system with modern UI
  - Login page at `/login/` (also serves as index `/`)
  - Dashboard at `/dashboard/` for authenticated users
  - Automatic redirection based on authentication status
  - Session management and logout functionality
- **Templates**: Bootstrap 5 with gradient design and responsive layout
- **Tests**: Basic test file exists but no test cases implemented

### 📊 **NEW: Invoice Management System**
- **CustomerVendor Model**: Supports customers, vendors, or both with proper type choices
- **InvoiceMaster Model**: Complete invoice management with:
  - Invoice types: Purchases, Sales, Return Purchases, Return Sales
  - Payment types: Cash, Visa, Partial/Deferred
  - Status tracking: Paid, Unpaid, Partially Paid
  - Return status: Not Returned, Partially Returned, Fully Returned
  - Discount and tax management at invoice level
- **InvoiceDetail Model**: Line item management with:
  - Item quantities, prices, discounts, taxes
  - Store-specific tracking
  - Proper foreign key relationships
- **Stock Management**: Real-time stock calculation via API endpoint `/api/stock/`
  - Calculates stock based on purchase and sales transactions
  - Supports filtering by item and store
  - Equivalent to PostgreSQL itemStock view

### 🔗 **API Endpoints Summary:**
#### Original Tables:
- `/api/items-groups/` - Items groups management
- `/api/items/` - Items management with group relationships
- `/api/price-lists/` - Price lists management
- `/api/price-list-details/` - Price list details with filtering
- `/api/store-groups/` - Store groups management
- `/api/stores/` - Stores management

#### New Invoice Tables:
- `/api/customers-vendors/` - Customer and vendor management with type filtering
- `/api/invoices/` - Invoice management with comprehensive filtering
- `/api/invoice-details/` - Invoice line items with relationships
- `/api/stock/` - Real-time stock calculations

### 🔐 Authentication System Features:
- **Index Page**: Root URL `/` redirects to login or dashboard based on auth status
- **Login Page**: Beautiful split-screen design with brand section and login form
- **Dashboard**: Complete overview with statistics, quick actions, and user info
- **Navigation**: Dynamic navbar that appears only for authenticated users
- **Session Management**: 24-hour sessions with proper logout handling
- **Responsive Design**: Works perfectly on mobile and desktop
- **Form Validation**: Client-side and server-side validation with Bootstrap styling

### 🎨 UI Design Features:
- **Modern Gradient**: Purple-blue gradient background and buttons
- **Split Layout**: Brand showcase on left, login form on right
- **Card Design**: Glassmorphism effect with backdrop blur
- **Icons**: Bootstrap Icons throughout the interface
- **Stats Cards**: Color-coded statistics with hover effects
- **Quick Actions**: Easy access to admin functions and API docs

### 🔄 Remaining Tasks:
1. **Write comprehensive tests** for all models, serializers, and views
2. **Add authentication/authorization** for API endpoints
3. **Implement user role management** system
4. **Add data validation** and error handling
5. **Performance optimization** and database indexing

### ✅ **FIXED ISSUES FROM REVIEW:**
- **Admin Registration**: All new models now properly registered in Django admin
- **Documentation**: Added comprehensive docstrings throughout codebase
- **Constants**: Created centralized constants.py for choice fields
- **Code Organization**: Improved with proper inlines and structured admin interfaces
- **Help Text**: Added helpful descriptions to all model fields
- **Fieldsets**: Organized admin interfaces with logical field groupings
- **Model Meta**: Added verbose names and proper model configuration

### 🆕 **NEW: Accounting System Implementation**
- **Account Model**: Complete account management for the accounting system with:
  - Account names and grouping
  - Unique sign/code system
  - Proper audit fields and user tracking
- **Transaction Model**: Comprehensive transaction tracking with:
  - Account relationships
  - Transaction types: Purchase, Sales, Return Purchase, Return Sales
  - Customer/Vendor associations
  - Invoice connections
  - Amount tracking with notes
- **API Endpoints**: New accounting endpoints added:
  - `/api/accounts/` - Account management with filtering and search
  - `/api/transactions/` - Transaction management with comprehensive filtering
- **Admin Interfaces**: Complete admin management for accounts and transactions
- **Database Tables**: New `accounts` and `transactions` tables created and migrated



