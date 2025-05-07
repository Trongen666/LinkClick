"""
Test authentication functionality
"""
import asyncio
import unittest
import requests
import os
import json
from pathlib import Path

# Base URL for the API
BASE_URL = "http://localhost:8000"

class TestAuth(unittest.TestCase):
    def setUp(self):
        """Set up test data"""
        self.test_user = {
            "username": "testuser",
            "phone_number": "1234567890"
        }
        self.admin_user = {
            "username": "admin",
            "phone_number": "1234567890"
        }
        self.test_token = None

    def test_01_register(self):
        """Test user registration"""
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=self.test_user
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertIn("User registered successfully", response.json()["message"])
        
    def test_02_request_otp(self):
        """Test OTP request"""
        response = requests.post(
            f"{BASE_URL}/auth/request-otp",
            json={"username": self.test_user["username"]}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("OTP sent successfully", response.json()["message"])
        
        # In a real test, we would need to intercept the OTP
        # For this test, we'll need to manually check the OTP from logs or database
        print("Please check the server logs for the OTP code sent to the test user")
        otp = input("Enter the OTP code: ")
        
        # Verify OTP
        response = requests.post(
            f"{BASE_URL}/auth/verify-otp",
            json={
                "username": self.test_user["username"],
                "otp_code": otp
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.test_token = response.json()["access_token"]
        
    def test_03_register_face(self):
        """Test face registration"""
        # For this test, you need a test face image
        test_image_path = Path(__file__).parent / "test_face.jpg"
        
        if not test_image_path.exists():
            self.skipTest(f"Test image {test_image_path} does not exist")
            
        with open(test_image_path, "rb") as f:
            files = {"face_image": f}
            headers = {"Authorization": f"Bearer {self.test_token}"}
            
            response = requests.post(
                f"{BASE_URL}/auth/register-face",
                files=files,
                headers=headers
            )
            
        self.assertEqual(response.status_code, 200)
        self.assertIn("Face registered successfully", response.json()["message"])
        
    def test_04_face_login(self):
        """Test face login"""
        # For this test, you need the same test face image
        test_image_path = Path(__file__).parent / "test_face.jpg"
        
        if not test_image_path.exists():
            self.skipTest(f"Test image {test_image_path} does not exist")
            
        with open(test_image_path, "rb") as f:
            files = {"face_image": f}
            data = {"username": self.test_user["username"]}
            
            response = requests.post(
                f"{BASE_URL}/auth/face-login",
                files=files,
                data=data
            )
            
        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        
    def test_05_user_management(self):
        """Test user management endpoints (admin only)"""
        # Login as admin first
        print("Please manually obtain an admin token for testing user management endpoints")
        admin_token = input("Enter admin token: ")
        
        # Get all users
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/users/",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        users = response.json()
        
        # Find our test user
        test_user_id = None
        for user in users:
            if user["username"] == self.test_user["username"]:
                test_user_id = user["id"]
                break
                
        self.assertIsNotNone(test_user_id, "Test user not found")
        
        # Deactivate user
        response = requests.put(
            f"{BASE_URL}/users/{test_user_id}/deactivate",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Get user info
        response = requests.get(
            f"{BASE_URL}/users/{test_user_id}",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_active"])
        
        # Activate user
        response = requests.put(
            f"{BASE_URL}/users/{test_user_id}/activate",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        
        # Get user info again
        response = requests.get(
            f"{BASE_URL}/users/{test_user_id}",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_active"])
        
    def test_06_cleanup(self):
        """Clean up test data"""
        # Login as admin first
        print("Please manually obtain an admin token for cleanup")
        admin_token = input("Enter admin token: ")
        
        # Get all users
        headers = {"Authorization": f"Bearer {admin_token}"}
        response = requests.get(
            f"{BASE_URL}/users/",
            headers=headers
        )
        
        self.assertEqual(response.status_code, 200)
        users = response.json()
        
        # Find our test user
        test_user_id = None
        for user in users:
            if user["username"] == self.test_user["username"]:
                test_user_id = user["id"]
                break
                
        if test_user_id:
            # Delete test user
            response = requests.delete(
                f"{BASE_URL}/users/{test_user_id}",
                headers=headers
            )
            
            self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()