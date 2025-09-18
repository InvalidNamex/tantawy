#!/usr/bin/env python3
"""
Invoice API Test Script
Tests the invoice creation API with sample data
"""

import json
import requests
from datetime import datetime

# Configuration
BASE_URL = "http://127.0.0.1:8000/core/api"
# Note: You'll need to replace this with actual authentication token
AUTH_TOKEN = "your_auth_token_here"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {AUTH_TOKEN}"
}

def test_purchase_invoice():
    """Test creating a purchase invoice"""
    print("Testing Purchase Invoice Creation...")
    
    data = {
        "invoiceMaster": {
            "invoiceType": 1,
            "customerOrVendorID": 1,  # Replace with valid vendor ID
            "storeId": 1,             # Replace with valid store ID
            "paymentType": 1,         # Cash
            "notes": "Test purchase invoice",
            "discountAmount": 0.00,
            "discountPercentage": 0.00,
            "taxAmount": 15.00,
            "taxPercentage": 15.00,
            "netTotal": 115.00,
            "status": 0,              # Paid
            "totalPaid": 115.00,
            "returnStatus": 0         # Not returned
        },
        "invoiceDetails": [
            {
                "item": 1,            # Replace with valid item ID
                "quantity": 2.0,
                "price": 50.00,
                "notes": "Test item",
                "discountAmount": 0.00,
                "discountPercentage": 0.00,
                "taxAmount": 15.00,
                "taxPercentage": 15.00
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/invoices/", 
                               json=data, 
                               headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get('invoiceId')
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    return None

def test_sales_invoice():
    """Test creating a sales invoice"""
    print("\nTesting Sales Invoice Creation...")
    
    data = {
        "invoiceMaster": {
            "invoiceType": 2,
            "customerOrVendorID": 2,  # Replace with valid customer ID
            "storeId": 1,             # Replace with valid store ID
            "paymentType": 2,         # Visa
            "notes": "Test sales invoice",
            "discountAmount": 5.00,
            "discountPercentage": 0.00,
            "taxAmount": 12.75,
            "taxPercentage": 15.00,
            "netTotal": 92.75,
            "status": 0,              # Paid
            "totalPaid": 92.75,
            "returnStatus": 0         # Not returned
        },
        "invoiceDetails": [
            {
                "item": 1,            # Replace with valid item ID
                "quantity": 3.0,
                "price": 30.00,
                "notes": "Test sale item",
                "discountAmount": 5.00,
                "discountPercentage": 0.00,
                "taxAmount": 12.75,
                "taxPercentage": 15.00
            }
        ]
    }
    
    try:
        response = requests.post(f"{BASE_URL}/invoices/", 
                               json=data, 
                               headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 201:
            return response.json().get('invoiceId')
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    
    return None

def test_get_invoices_by_type(invoice_type):
    """Test getting invoices by type"""
    print(f"\nTesting Get Invoices by Type {invoice_type}...")
    
    try:
        response = requests.get(f"{BASE_URL}/invoices/type/{invoice_type}/", 
                              headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def test_get_invoice_detail(invoice_id):
    """Test getting invoice details"""
    if not invoice_id:
        print("\nSkipping invoice detail test - no valid invoice ID")
        return
        
    print(f"\nTesting Get Invoice Detail for ID {invoice_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/invoices/{invoice_id}/", 
                              headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def test_available_returns(invoice_id):
    """Test getting available returns"""
    if not invoice_id:
        print("\nSkipping available returns test - no valid invoice ID")
        return
        
    print(f"\nTesting Available Returns for Invoice {invoice_id}...")
    
    try:
        response = requests.get(f"{BASE_URL}/invoices/{invoice_id}/available-returns/", 
                              headers=headers)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def main():
    """Run all tests"""
    print("=== Invoice API Test Script ===")
    print(f"Testing against: {BASE_URL}")
    print(f"Timestamp: {datetime.now()}")
    print("=" * 50)
    
    # Test purchase invoice creation
    purchase_invoice_id = test_purchase_invoice()
    
    # Test sales invoice creation
    sales_invoice_id = test_sales_invoice()
    
    # Test getting invoices by type
    test_get_invoices_by_type(1)  # Purchase invoices
    test_get_invoices_by_type(2)  # Sales invoices
    
    # Test getting invoice details
    test_get_invoice_detail(purchase_invoice_id)
    test_get_invoice_detail(sales_invoice_id)
    
    # Test available returns
    test_available_returns(purchase_invoice_id)
    test_available_returns(sales_invoice_id)
    
    print("\n=== Test Script Complete ===")

if __name__ == "__main__":
    main()