#!/usr/bin/env python3
"""
Test script for ParsePhish API
"""

import requests
import json
import time

API_BASE = "http://localhost:8080"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    response = requests.get(f"{API_BASE}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_email_analysis():
    """Test email analysis endpoint"""
    print("\n📧 Testing email analysis...")
    
    test_cases = [
        {
            "content": "Urgent! Your account will be suspended in 24 hours. Click here to verify your identity immediately.",
            "subject": "Account Security Alert"
        },
        {
            "content": "Thank you for your purchase. Your order will be shipped within 2-3 business days.",
            "subject": "Order Confirmation"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n  Test {i}: {test_case['subject']}")
        response = requests.post(
            f"{API_BASE}/analyze/email",
            json=test_case,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"    Score: {result['phishy_score']:.2f}")
            print(f"    Verdict: {result['verdict']}")
            print(f"    Suspect phrases: {result['suspect_phrases']}")
        else:
            print(f"    Error: {response.status_code} - {response.text}")

def test_url_analysis():
    """Test URL analysis endpoint"""
    print("\n🔗 Testing URL analysis...")
    
    test_case = {
        "url": "https://www.google.com"
    }
    
    response = requests.post(
        f"{API_BASE}/analyze/url",
        json=test_case,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"  Score: {result['phishy_score']:.2f}")
        print(f"  Verdict: {result['verdict']}")
        print(f"  Suspect phrases: {result['suspect_phrases']}")
    else:
        print(f"  Error: {response.status_code} - {response.text}")

def main():
    print("🧪 ParsePhish API Test Suite")
    print("="*50)
    
    # Wait a moment for the server to be ready
    print("⏳ Waiting for API to be ready...")
    time.sleep(2)
    
    try:
        # Test health
        if test_health():
            print("✅ Health check passed")
            
            # Test email analysis
            test_email_analysis()
            
            # Test URL analysis
            test_url_analysis()
            
            print("\n🎉 All tests completed!")
        else:
            print("❌ Health check failed")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to API. Make sure the server is running.")
        print("   Run: python main.py")

if __name__ == "__main__":
    main()