"""
Constants for the core application.
Contains choice field constants for models to ensure consistency and maintainability.
"""

# CustomerVendor Type Choices
CUSTOMER_VENDOR_TYPE_CHOICES = [
    (1, 'Customer'),
    (2, 'Vendor'),
    (3, 'Both'),
]

# Invoice Type Choices
INVOICE_TYPE_CHOICES = [
    (1, 'Purchases'),
    (2, 'Sales'),
    (3, 'Return Purchases'),
    (4, 'Return Sales'),
]

# Payment Type Choices
PAYMENT_TYPE_CHOICES = [
    (1, 'Cash'),
    (2, 'Visa'),
    (3, 'Partial or Deferred'),
]

# Invoice Status Choices
INVOICE_STATUS_CHOICES = [
    (0, 'Paid'),
    (1, 'Unpaid'),
    (2, 'Partially Paid'),
]

# Return Status Choices
RETURN_STATUS_CHOICES = [
    (0, 'Not Returned'),
    (1, 'Partially Returned'),
    (2, 'Fully Returned'),
]

# Constants for Invoice Types
INVOICE_TYPE_PURCHASES = 1
INVOICE_TYPE_SALES = 2
INVOICE_TYPE_RETURN_PURCHASES = 3
INVOICE_TYPE_RETURN_SALES = 4

# Constants for Payment Types
PAYMENT_TYPE_CASH = 1
PAYMENT_TYPE_VISA = 2
PAYMENT_TYPE_PARTIAL_DEFERRED = 3

# Constants for Status
STATUS_PAID = 0
STATUS_UNPAID = 1
STATUS_PARTIALLY_PAID = 2

# Constants for Return Status
RETURN_STATUS_NOT_RETURNED = 0
RETURN_STATUS_PARTIALLY_RETURNED = 1
RETURN_STATUS_FULLY_RETURNED = 2

# Transaction Type Choices
TRANSACTION_TYPE_CHOICES = [
    (1, 'Purchase'),
    (2, 'Sales'),
    (3, 'Return Purchase'),
    (4, 'Return Sales'),
]

# Constants for Transaction Types
TRANSACTION_TYPE_PURCHASE = 1
TRANSACTION_TYPE_SALES = 2
TRANSACTION_TYPE_RETURN_PURCHASE = 3
TRANSACTION_TYPE_RETURN_SALES = 4

# Agent related constants
AGENT_MAX_NAME_LENGTH = 255

# Agent Status Constants (for future use if needed)
AGENT_STATUS_ACTIVE = 1
AGENT_STATUS_INACTIVE = 0

# Visit Transaction Type Choices
VISIT_TRANSACTION_TYPE_CHOICES = [
    (1, 'Sales'),
    (2, 'Return Sales'),
    (3, 'Receive Voucher'),
    (4, 'Pay Voucher'),
    (5, 'Negative Visit'),
]

# Constants for Visit Transaction Types
VISIT_TRANSACTION_TYPE_SALES = 1
VISIT_TRANSACTION_TYPE_RETURN_SALES = 2
VISIT_TRANSACTION_TYPE_RECEIVE_VOUCHER = 3
VISIT_TRANSACTION_TYPE_PAY_VOUCHER = 4
VISIT_TRANSACTION_TYPE_NEGATIVE_VISIT = 5