#!/usr/bin/env python
"""
Test script for Agent Authentication System
Tests the agent login, logout, and token verification endpoints.
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/core"

def test_agent_authentication():
    print("🧪 Testing Agent Authentication System")
    print("=" * 50)
    
    # Test 1: Create an agent
    print("\n1. Creating test agent...")
    create_data = {
        "agentName": "Test Agent Updated",
        "agentUsername": "testagent_updated", 
        "agentPhone": "123456789",
        "password": "testpass123",
        "isActive": True
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/agents/create/", json=create_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 201:
            print("   ✅ Agent created successfully!")
        else:
            print("   ❌ Failed to create agent")
            return
    except Exception as e:
        print(f"   ❌ Error creating agent: {e}")
        return
    
    # Test 2: Agent Login
    print("\n2. Testing agent login...")
    login_data = {
        "username": "testagent_updated",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/agents/login/", json=login_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 200:
            login_result = response.json()
            if login_result.get('success'):
                token = login_result.get('token')
                agent_data = login_result.get('agent')
                print("   ✅ Login successful!")
                print(f"   📱 Token: {token}")
                print(f"   👤 Agent: {agent_data['agentName']} ({agent_data['agentUsername']})")
                
                # Test 3: Token Verification
                print("\n3. Testing token verification...")
                try:
                    verify_response = requests.get(f"{BASE_URL}/api/agents/verify-token/?token={token}")
                    print(f"   Status: {verify_response.status_code}")
                    print(f"   Response: {verify_response.text}")
                    
                    if verify_response.status_code == 200:
                        verify_result = verify_response.json()
                        if verify_result.get('success'):
                            print("   ✅ Token verification successful!")
                        else:
                            print("   ❌ Token verification failed")
                    else:
                        print("   ❌ Token verification request failed")
                except Exception as e:
                    print(f"   ❌ Error verifying token: {e}")
                
                # Test 4: Agent Logout
                print("\n4. Testing agent logout...")
                logout_data = {"token": token}
                try:
                    logout_response = requests.post(f"{BASE_URL}/api/agents/logout/", json=logout_data)
                    print(f"   Status: {logout_response.status_code}")
                    print(f"   Response: {logout_response.text}")
                    
                    if logout_response.status_code == 200:
                        logout_result = logout_response.json()
                        if logout_result.get('success'):
                            print("   ✅ Logout successful!")
                        else:
                            print("   ❌ Logout failed")
                    else:
                        print("   ❌ Logout request failed")
                except Exception as e:
                    print(f"   ❌ Error during logout: {e}")
                    
            else:
                print("   ❌ Login failed")
        else:
            print("   ❌ Login request failed")
    except Exception as e:
        print(f"   ❌ Error during login: {e}")
    
    # Test 5: Invalid credentials
    print("\n5. Testing invalid credentials...")
    invalid_login_data = {
        "username": "testagent",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/agents/login/", json=invalid_login_data)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        
        if response.status_code == 401:
            print("   ✅ Invalid credentials properly rejected!")
        else:
            print("   ❌ Invalid credentials test failed")
    except Exception as e:
        print(f"   ❌ Error testing invalid credentials: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Agent Authentication System Testing Complete!")

if __name__ == "__main__":
    test_agent_authentication()