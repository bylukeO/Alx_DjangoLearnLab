#!/usr/bin/env python
"""
Test script to demonstrate the custom user model functionality.
Run this script to test user creation with the custom user model.
"""

import os
import sys
import django
from datetime import date

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from accounts.models import CustomUser

def test_custom_user_creation():
    """Test creating users with the custom user model."""
    
    print("Testing Custom User Model")
    print("=" * 50)
    
    # Test creating a regular user
    try:
        user = CustomUser.objects.create_user(
            email='john.doe@example.com',
            password='secure_password123',
            first_name='John',
            last_name='Doe',
            date_of_birth=date(1990, 5, 15)
        )
        print(f"[SUCCESS] Regular user created successfully: {user}")
        print(f"  - Email: {user.email}")
        print(f"  - Full Name: {user.get_full_name()}")
        print(f"  - Age: {user.age}")
        print(f"  - Is Staff: {user.is_staff}")
        print(f"  - Is Superuser: {user.is_superuser}")
        
    except Exception as e:
        print(f"[ERROR] Error creating regular user: {e}")
    
    print()
    
    # Test creating a superuser
    try:
        admin_user = CustomUser.objects.create_superuser(
            email='admin@example.com',
            password='admin_password123',
            first_name='Admin',
            last_name='User',
            date_of_birth=date(1985, 10, 20)
        )
        print(f"[SUCCESS] Superuser created successfully: {admin_user}")
        print(f"  - Email: {admin_user.email}")
        print(f"  - Full Name: {admin_user.get_full_name()}")
        print(f"  - Age: {admin_user.age}")
        print(f"  - Is Staff: {admin_user.is_staff}")
        print(f"  - Is Superuser: {admin_user.is_superuser}")
        
    except Exception as e:
        print(f"[ERROR] Error creating superuser: {e}")
    
    print()
    print("Custom User Model Test Complete!")
    print(f"Total users in database: {CustomUser.objects.count()}")

if __name__ == '__main__':
    test_custom_user_creation()